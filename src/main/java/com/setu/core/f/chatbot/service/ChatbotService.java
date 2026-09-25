package com.setu.core.f.chatbot.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.setu.core.a.auth.entity.User;
import com.setu.core.a.auth.repository.UserRepository;
import com.setu.core.c.project.entity.Project;
import com.setu.core.c.project.repository.ProjectRepository;
import com.setu.core.e.risk.entity.RiskScore;
import com.setu.core.e.risk.repository.RiskScoreRepository;
import com.setu.core.f.chatbot.client.ChatbotServiceClient;
import com.setu.core.f.chatbot.dto.*;
import com.setu.core.f.chatbot.entity.*;
import com.setu.core.f.chatbot.repository.ChatMessageRepository;
import com.setu.core.f.chatbot.repository.ChatSessionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class ChatbotService {

    @Autowired
    private ChatSessionRepository sessionRepository;

    @Autowired
    private ChatMessageRepository messageRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private RiskScoreRepository riskScoreRepository;

    @Autowired
    private ChatbotServiceClient chatbotServiceClient;

    private final ObjectMapper objectMapper = new ObjectMapper();

    public ChatResponseDTO query(ChatQueryDTO queryDTO, String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        ChatSession session;
        Project project = null;

        if (queryDTO.getSessionId() != null) {
            session = sessionRepository.findById(queryDTO.getSessionId())
                    .orElseThrow(() -> new IllegalArgumentException("Session not found"));
            project = session.getProject();
        } else {
            session = new ChatSession();
            session.setUser(user);
            if (queryDTO.getProjectId() != null) {
                project = projectRepository.findById(queryDTO.getProjectId())
                        .orElseThrow(() -> new IllegalArgumentException("Project not found"));
                session.setProject(project);
            }
            session = sessionRepository.save(session);
        }

        // Save user's message
        ChatMessage userMessage = new ChatMessage();
        userMessage.setSession(session);
        userMessage.setSender(Sender.USER);
        userMessage.setContent(queryDTO.getQuestion());
        messageRepository.save(userMessage);

        // Build user_project: must be the exact project_data blob his /predict
        // call returned, not a hand-built object — his code expects those
        // exact engineered fields.
        Map<String, Object> userProject = null;
        if (project != null) {
            RiskScore latestRiskScore = riskScoreRepository
                    .findTopByProject_ProjectIdOrderByGeneratedAtDesc(project.getProjectId())
                    .orElse(null);

            if (latestRiskScore != null && latestRiskScore.getMlProjectDataJson() != null) {
                try {
                    userProject = objectMapper.readValue(latestRiskScore.getMlProjectDataJson(), Map.class);
                } catch (Exception e) {
                    userProject = null;
                }
            }
        }

        // Build history in his expected shape: role ("user"/"model") + text
        List<Map<String, String>> history = messageRepository
                .findBySession_SessionIdOrderByTimestampAsc(session.getSessionId())
                .stream()
                .map(m -> {
                    Map<String, String> entry = new HashMap<>();
                    entry.put("role", m.getSender() == Sender.USER ? "user" : "model");
                    entry.put("text", m.getContent());
                    return entry;
                })
                .collect(Collectors.toList());

        // Call external chatbot microservice — his schema now requires session_id too
        String answer = chatbotServiceClient.getAnswer(
                session.getSessionId(),
                queryDTO.getQuestion(),
                userProject,
                history
        );

        // Save bot's response
        ChatMessage botMessage = new ChatMessage();
        botMessage.setSession(session);
        botMessage.setSender(Sender.BOT);
        botMessage.setContent(answer);
        messageRepository.save(botMessage);

        session.setLastMessageAt(LocalDateTime.now());
        sessionRepository.save(session);

        return new ChatResponseDTO(session.getSessionId(), answer);
    }

    public List<ChatMessageDTO> getHistory(Long sessionId) {
        return messageRepository.findBySession_SessionIdOrderByTimestampAsc(sessionId)
                .stream()
                .map(m -> new ChatMessageDTO(m.getSender().name(), m.getContent(), m.getTimestamp()))
                .collect(Collectors.toList());
    }

    public List<Long> getUserSessions(String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        return sessionRepository.findByUser_UserIdOrderByLastMessageAtDesc(user.getUserId())
                .stream()
                .map(ChatSession::getSessionId)
                .collect(Collectors.toList());
    }
}
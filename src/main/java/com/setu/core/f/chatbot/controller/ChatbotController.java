package com.setu.core.f.chatbot.controller;

import com.setu.core.f.chatbot.dto.ChatMessageDTO;
import com.setu.core.f.chatbot.dto.ChatQueryDTO;
import com.setu.core.f.chatbot.dto.ChatResponseDTO;
import com.setu.core.f.chatbot.service.ChatbotService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/chatbot")
public class ChatbotController {

    @Autowired
    private ChatbotService chatbotService;

    @PostMapping("/query")
    public ResponseEntity<ChatResponseDTO> query(@RequestBody ChatQueryDTO queryDTO,
                                                 @AuthenticationPrincipal String userEmail) {
        return ResponseEntity.ok(chatbotService.query(queryDTO, userEmail));
    }

    @GetMapping("/sessions/{sessionId}/messages")
    public ResponseEntity<List<ChatMessageDTO>> getHistory(@PathVariable Long sessionId) {
        return ResponseEntity.ok(chatbotService.getHistory(sessionId));
    }

    @GetMapping("/sessions")
    public ResponseEntity<List<Long>> getSessions(@AuthenticationPrincipal String userEmail) {
        return ResponseEntity.ok(chatbotService.getUserSessions(userEmail));
    }
}
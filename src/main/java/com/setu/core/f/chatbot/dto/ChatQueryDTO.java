package com.setu.core.f.chatbot.dto;

public class ChatQueryDTO {

    private Long sessionId;   // null if starting a new session
    private Long projectId;   // optional
    private String question;

    public Long getSessionId() {
        return sessionId;
    }

    public void setSessionId(Long sessionId) {
        this.sessionId = sessionId;
    }

    public Long getProjectId() {
        return projectId;
    }

    public void setProjectId(Long projectId) {
        this.projectId = projectId;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }
}
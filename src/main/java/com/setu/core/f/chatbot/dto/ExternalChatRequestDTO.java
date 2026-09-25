package com.setu.core.f.chatbot.dto;

import java.util.List;
import java.util.Map;

public class ExternalChatRequestDTO {

    private String message;
    private String session_id;
    private Map<String, Object> user_project;
    private List<Map<String, String>> history;

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getSession_id() {
        return session_id;
    }

    public void setSession_id(String session_id) {
        this.session_id = session_id;
    }

    public Map<String, Object> getUser_project() {
        return user_project;
    }

    public void setUser_project(Map<String, Object> user_project) {
        this.user_project = user_project;
    }

    public List<Map<String, String>> getHistory() {
        return history;
    }

    public void setHistory(List<Map<String, String>> history) {
        this.history = history;
    }
}
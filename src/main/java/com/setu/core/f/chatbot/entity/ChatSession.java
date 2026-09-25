package com.setu.core.f.chatbot.entity;

import com.setu.core.a.auth.entity.User;
import com.setu.core.c.project.entity.Project;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "chat_sessions")
public class ChatSession {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long sessionId;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne
    @JoinColumn(name = "project_id")
    private Project project;   // optional — chat may or may not be scoped to a project

    @Column(nullable = false, updatable = false)
    private LocalDateTime startedAt;

    private LocalDateTime lastMessageAt;

    @PrePersist
    protected void onCreate() {
        this.startedAt = LocalDateTime.now();
        this.lastMessageAt = LocalDateTime.now();
    }

    public Long getSessionId() {
        return sessionId;
    }

    public void setSessionId(Long sessionId) {
        this.sessionId = sessionId;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public LocalDateTime getStartedAt() {
        return startedAt;
    }

    public void setStartedAt(LocalDateTime startedAt) {
        this.startedAt = startedAt;
    }

    public LocalDateTime getLastMessageAt() {
        return lastMessageAt;
    }

    public void setLastMessageAt(LocalDateTime lastMessageAt) {
        this.lastMessageAt = lastMessageAt;
    }
}
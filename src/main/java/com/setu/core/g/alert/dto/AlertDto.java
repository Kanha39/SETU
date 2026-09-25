package com.setu.core.g.alert.dto;

import java.time.LocalDateTime;

public class AlertDto {

    private Long alertId;
    private Long projectId;
    private String projectName;
    private String severity;
    private String message;
    private boolean acknowledged;
    private LocalDateTime createdAt;

    public AlertDto(Long alertId, Long projectId, String projectName, String severity,
                    String message, boolean acknowledged, LocalDateTime createdAt) {
        this.alertId = alertId;
        this.projectId = projectId;
        this.projectName = projectName;
        this.severity = severity;
        this.message = message;
        this.acknowledged = acknowledged;
        this.createdAt = createdAt;
    }

    public Long getAlertId() {
        return alertId;
    }

    public Long getProjectId() {
        return projectId;
    }

    public String getProjectName() {
        return projectName;
    }

    public String getSeverity() {
        return severity;
    }

    public String getMessage() {
        return message;
    }

    public boolean isAcknowledged() {
        return acknowledged;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}

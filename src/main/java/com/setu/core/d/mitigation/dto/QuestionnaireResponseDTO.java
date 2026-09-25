package com.setu.core.d.mitigation.dto;

public class QuestionnaireResponseDTO {
    private String projectName;
    private Integer sessionId;

    public QuestionnaireResponseDTO(String projectName, Integer sessionId) {
        this.projectName = projectName;
        this.sessionId = sessionId;
    }

    public String getProjectName() { return projectName; }
    public Integer getSessionId() { return sessionId; }
}
package com.setu.core.h.dashboard.dto;

public class TopRiskProjectDTO {

    private final Long projectId;
    private final String name;
    private final Double riskScoreValue;
    private final String riskLevel;

    public TopRiskProjectDTO(Long projectId, String name, Double riskScoreValue, String riskLevel) {
        this.projectId = projectId;
        this.name = name;
        this.riskScoreValue = riskScoreValue;
        this.riskLevel = riskLevel;
    }

    public Long getProjectId() {
        return projectId;
    }

    public String getName() {
        return name;
    }

    public Double getRiskScoreValue() {
        return riskScoreValue;
    }

    public String getRiskLevel() {
        return riskLevel;
    }
}


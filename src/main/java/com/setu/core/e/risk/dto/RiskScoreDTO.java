package com.setu.core.e.risk.dto;

import java.time.LocalDateTime;

public class RiskScoreDTO {

    private Long projectId;
    private Double riskScoreValue;
    private String riskLevel;
    private String contributingFactors;
    private LocalDateTime generatedAt;

    public RiskScoreDTO(Long projectId, Double riskScoreValue, String riskLevel,
                        String contributingFactors, LocalDateTime generatedAt) {
        this.projectId = projectId;
        this.riskScoreValue = riskScoreValue;
        this.riskLevel = riskLevel;
        this.contributingFactors = contributingFactors;
        this.generatedAt = generatedAt;
    }

    public Long getProjectId() {
        return projectId;
    }

    public void setProjectId(Long projectId) {
        this.projectId = projectId;
    }

    public Double getRiskScoreValue() {
        return riskScoreValue;
    }

    public void setRiskScoreValue(Double riskScoreValue) {
        this.riskScoreValue = riskScoreValue;
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }

    public String getContributingFactors() {
        return contributingFactors;
    }

    public void setContributingFactors(String contributingFactors) {
        this.contributingFactors = contributingFactors;
    }

    public LocalDateTime getGeneratedAt() {
        return generatedAt;
    }

    public void setGeneratedAt(LocalDateTime generatedAt) {
        this.generatedAt = generatedAt;
    }
}
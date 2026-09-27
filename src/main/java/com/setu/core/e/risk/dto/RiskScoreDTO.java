package com.setu.core.e.risk.dto;

import java.time.LocalDateTime;

public class RiskScoreDTO {
    private Long projectId;
    private Double riskScoreValue;
    private String riskLevel;
    private String contributingFactors;
    private LocalDateTime generatedAt;
    private Double predictedOverrunPct;
    private Double predictedDelayDays;
    private String costRiskLevel;
    private String timeRiskLevel;

    public RiskScoreDTO(Long projectId, Double riskScoreValue, String riskLevel,
                        String contributingFactors, LocalDateTime generatedAt,
                        Double predictedOverrunPct, Double predictedDelayDays,
                        String costRiskLevel, String timeRiskLevel) {
        this.projectId = projectId;
        this.riskScoreValue = riskScoreValue;
        this.riskLevel = riskLevel;
        this.contributingFactors = contributingFactors;
        this.generatedAt = generatedAt;
        this.predictedOverrunPct = predictedOverrunPct;
        this.predictedDelayDays = predictedDelayDays;
        this.costRiskLevel = costRiskLevel;
        this.timeRiskLevel = timeRiskLevel;
    }

    public Long getProjectId() { return projectId; }
    public Double getRiskScoreValue() { return riskScoreValue; }
    public String getRiskLevel() { return riskLevel; }
    public String getContributingFactors() { return contributingFactors; }
    public LocalDateTime getGeneratedAt() { return generatedAt; }
    public Double getPredictedOverrunPct() { return predictedOverrunPct; }
    public Double getPredictedDelayDays() { return predictedDelayDays; }
    public String getCostRiskLevel() { return costRiskLevel; }
    public String getTimeRiskLevel() { return timeRiskLevel; }
}
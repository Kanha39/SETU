package com.setu.core.d.mitigation.dto;

import java.time.LocalDateTime;

public class MitigationStrategyDTO {
    private String projectName;
    private Integer sessionId;
    private Integer strategyId;
    private String mitigationStrategy;
    private LocalDateTime generatedAt;

    public MitigationStrategyDTO(String projectName, Integer sessionId, Integer strategyId,
                                 String mitigationStrategy, LocalDateTime generatedAt) {
        this.projectName = projectName;
        this.sessionId = sessionId;
        this.strategyId = strategyId;
        this.mitigationStrategy = mitigationStrategy;
        this.generatedAt = generatedAt;
    }

    public String getProjectName() { return projectName; }
    public Integer getSessionId() { return sessionId; }
    public Integer getStrategyId() { return strategyId; }
    public String getMitigationStrategy() { return mitigationStrategy; }
    public LocalDateTime getGeneratedAt() { return generatedAt; }
}
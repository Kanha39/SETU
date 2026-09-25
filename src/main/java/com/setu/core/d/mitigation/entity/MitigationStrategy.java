package com.setu.core.d.mitigation.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "mitigation_strategies")
public class MitigationStrategy {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long strategyRecordId;

    @Column(name = "project_name", nullable = false)
    private String projectName;

    @Column(name = "session_id", nullable = false)
    private Integer sessionId;

    @Column(name = "strategy_id", nullable = false)
    private Integer strategyId;

    @Column(name = "mitigation_strategy", nullable = false, columnDefinition = "TEXT")
    private String mitigationStrategy;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    public Long getStrategyRecordId() { return strategyRecordId; }
    public void setStrategyRecordId(Long strategyRecordId) { this.strategyRecordId = strategyRecordId; }
    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }
    public Integer getSessionId() { return sessionId; }
    public void setSessionId(Integer sessionId) { this.sessionId = sessionId; }
    public Integer getStrategyId() { return strategyId; }
    public void setStrategyId(Integer strategyId) { this.strategyId = strategyId; }
    public String getMitigationStrategy() { return mitigationStrategy; }
    public void setMitigationStrategy(String mitigationStrategy) { this.mitigationStrategy = mitigationStrategy; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}

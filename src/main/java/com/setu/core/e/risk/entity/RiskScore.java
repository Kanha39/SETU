package com.setu.core.e.risk.entity;

import com.setu.core.c.project.entity.Project;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "risk_scores")
public class RiskScore {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long riskScoreId;

    @ManyToOne
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @Column(nullable = false)
    private Double riskScoreValue;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private RiskLevel riskLevel;

    private Double predictedOverrunPct;

    private Double predictedDelayDays;

    @Enumerated(EnumType.STRING)
    private RiskLevel costRiskLevel;

    @Enumerated(EnumType.STRING)
    private RiskLevel timeRiskLevel;

    @Column(columnDefinition = "TEXT")
    private String contributingFactors;

    @Column(columnDefinition = "LONGTEXT")
    private String mlProjectDataJson;

    @Column(nullable = false)
    private String modelVersion;

    @Column(nullable = false, updatable = false)
    private LocalDateTime generatedAt;

    @PrePersist
    protected void onCreate() {
        this.generatedAt = LocalDateTime.now();
    }

    public Long getRiskScoreId() {
        return riskScoreId;
    }

    public void setRiskScoreId(Long riskScoreId) {
        this.riskScoreId = riskScoreId;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public Double getRiskScoreValue() {
        return riskScoreValue;
    }

    public void setRiskScoreValue(Double riskScoreValue) {
        this.riskScoreValue = riskScoreValue;
    }

    public RiskLevel getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(RiskLevel riskLevel) {
        this.riskLevel = riskLevel;
    }

    public Double getPredictedOverrunPct() {
        return predictedOverrunPct;
    }

    public void setPredictedOverrunPct(Double predictedOverrunPct) {
        this.predictedOverrunPct = predictedOverrunPct;
    }

    public Double getPredictedDelayDays() {
        return predictedDelayDays;
    }

    public void setPredictedDelayDays(Double predictedDelayDays) {
        this.predictedDelayDays = predictedDelayDays;
    }

    public RiskLevel getCostRiskLevel() {
        return costRiskLevel;
    }

    public void setCostRiskLevel(RiskLevel costRiskLevel) {
        this.costRiskLevel = costRiskLevel;
    }

    public RiskLevel getTimeRiskLevel() {
        return timeRiskLevel;
    }

    public void setTimeRiskLevel(RiskLevel timeRiskLevel) {
        this.timeRiskLevel = timeRiskLevel;
    }

    public String getContributingFactors() {
        return contributingFactors;
    }

    public void setContributingFactors(String contributingFactors) {
        this.contributingFactors = contributingFactors;
    }

    public String getMlProjectDataJson() {
        return mlProjectDataJson;
    }

    public void setMlProjectDataJson(String mlProjectDataJson) {
        this.mlProjectDataJson = mlProjectDataJson;
    }

    public String getModelVersion() {
        return modelVersion;
    }

    public void setModelVersion(String modelVersion) {
        this.modelVersion = modelVersion;
    }

    public LocalDateTime getGeneratedAt() {
        return generatedAt;
    }

    public void setGeneratedAt(LocalDateTime generatedAt) {
        this.generatedAt = generatedAt;
    }
}
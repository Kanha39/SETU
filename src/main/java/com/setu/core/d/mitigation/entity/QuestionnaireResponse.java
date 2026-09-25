package com.setu.core.d.mitigation.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "questionnaire_responses")
public class QuestionnaireResponse {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long responseId;

    @Column(name = "project_name", nullable = false)
    private String projectName;

    @Column(name = "session_id", nullable = false)
    private Integer sessionId;

    @Column(name = "land_acquisition", length = 50)
    private String landAcquisition;

    @Column(name = "financial_result", length = 50)
    private String financialResult;

    @Column(name = "approval_clearance", length = 50)
    private String approvalClearance;

    @Column(name = "scope_design", length = 50)
    private String scopeDesign;

    @Column(name = "procurement_result", length = 50)
    private String procurementResult;

    @Column(name = "execution_pace", length = 50)
    private String executionPace;

    @Column(name = "interagency_coordination", length = 50)
    private String interagencyCoordination;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    public Long getResponseId() { return responseId; }
    public void setResponseId(Long responseId) { this.responseId = responseId; }
    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }
    public Integer getSessionId() { return sessionId; }
    public void setSessionId(Integer sessionId) { this.sessionId = sessionId; }
    public String getLandAcquisition() { return landAcquisition; }
    public void setLandAcquisition(String landAcquisition) { this.landAcquisition = landAcquisition; }
    public String getFinancialResult() { return financialResult; }
    public void setFinancialResult(String financialResult) { this.financialResult = financialResult; }
    public String getApprovalClearance() { return approvalClearance; }
    public void setApprovalClearance(String approvalClearance) { this.approvalClearance = approvalClearance; }
    public String getScopeDesign() { return scopeDesign; }
    public void setScopeDesign(String scopeDesign) { this.scopeDesign = scopeDesign; }
    public String getProcurementResult() { return procurementResult; }
    public void setProcurementResult(String procurementResult) { this.procurementResult = procurementResult; }
    public String getExecutionPace() { return executionPace; }
    public void setExecutionPace(String executionPace) { this.executionPace = executionPace; }
    public String getInteragencyCoordination() { return interagencyCoordination; }
    public void setInteragencyCoordination(String interagencyCoordination) { this.interagencyCoordination = interagencyCoordination; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}




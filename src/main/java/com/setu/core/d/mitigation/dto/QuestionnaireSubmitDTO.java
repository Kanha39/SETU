package com.setu.core.d.mitigation.dto;

import jakarta.validation.constraints.NotBlank;

public class QuestionnaireSubmitDTO {

    @NotBlank
    private String projectName;

    private String landAcquisition;
    private String financialResult;
    private String approvalClearance;
    private String scopeDesign;
    private String procurementResult;
    private String executionPace;
    private String interagencyCoordination;

    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }
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
}
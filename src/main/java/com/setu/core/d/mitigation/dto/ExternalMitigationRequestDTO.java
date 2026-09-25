package com.setu.core.d.mitigation.dto;

public class ExternalMitigationRequestDTO {

    private String session_id;
    private String project_name;
    private String land_acquisition;
    private String financial_result;
    private String approval_clearance;
    private String procurement_result;
    private String scope_design;
    private String execution_pace;
    private String interagency_coordination;
    private String created_at;

    public String getSession_id() { return session_id; }
    public void setSession_id(String session_id) { this.session_id = session_id; }
    public String getProject_name() { return project_name; }
    public void setProject_name(String project_name) { this.project_name = project_name; }
    public String getLand_acquisition() { return land_acquisition; }
    public void setLand_acquisition(String land_acquisition) { this.land_acquisition = land_acquisition; }
    public String getFinancial_result() { return financial_result; }
    public void setFinancial_result(String financial_result) { this.financial_result = financial_result; }
    public String getApproval_clearance() { return approval_clearance; }
    public void setApproval_clearance(String approval_clearance) { this.approval_clearance = approval_clearance; }
    public String getProcurement_result() { return procurement_result; }
    public void setProcurement_result(String procurement_result) { this.procurement_result = procurement_result; }
    public String getScope_design() { return scope_design; }
    public void setScope_design(String scope_design) { this.scope_design = scope_design; }
    public String getExecution_pace() { return execution_pace; }
    public void setExecution_pace(String execution_pace) { this.execution_pace = execution_pace; }
    public String getInteragency_coordination() { return interagency_coordination; }
    public void setInteragency_coordination(String interagency_coordination) { this.interagency_coordination = interagency_coordination; }
    public String getCreated_at() { return created_at; }
    public void setCreated_at(String created_at) { this.created_at = created_at; }
}
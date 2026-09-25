package com.setu.core.e.risk.dto;

public class MLRequestDTO {

    private String project_name;
    private String agency;
    private String state;
    private String ministry;
    private String sector;
    private String status;
    private Double original_cost_cr;
    private Double cumulative_expenditure;
    private Double physical_progress;
    private String date_of_approval;
    private String start_date;
    private String target_doc;

    public String getProject_name() {
        return project_name;
    }

    public void setProject_name(String project_name) {
        this.project_name = project_name;
    }

    public String getAgency() {
        return agency;
    }

    public void setAgency(String agency) {
        this.agency = agency;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getMinistry() {
        return ministry;
    }

    public void setMinistry(String ministry) {
        this.ministry = ministry;
    }

    public String getSector() {
        return sector;
    }

    public void setSector(String sector) {
        this.sector = sector;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Double getOriginal_cost_cr() {
        return original_cost_cr;
    }

    public void setOriginal_cost_cr(Double original_cost_cr) {
        this.original_cost_cr = original_cost_cr;
    }

    public Double getCumulative_expenditure() {
        return cumulative_expenditure;
    }

    public void setCumulative_expenditure(Double cumulative_expenditure) {
        this.cumulative_expenditure = cumulative_expenditure;
    }

    public Double getPhysical_progress() {
        return physical_progress;
    }

    public void setPhysical_progress(Double physical_progress) {
        this.physical_progress = physical_progress;
    }

    public String getDate_of_approval() {
        return date_of_approval;
    }

    public void setDate_of_approval(String date_of_approval) {
        this.date_of_approval = date_of_approval;
    }

    public String getStart_date() {
        return start_date;
    }

    public void setStart_date(String start_date) {
        this.start_date = start_date;
    }

    public String getTarget_doc() {
        return target_doc;
    }

    public void setTarget_doc(String target_doc) {
        this.target_doc = target_doc;
    }
}
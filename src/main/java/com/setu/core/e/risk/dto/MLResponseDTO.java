package com.setu.core.e.risk.dto;

import java.util.Map;

public class MLResponseDTO {

    private Predictions predictions;
    private Map<String, Object> project_data;

    public Predictions getPredictions() {
        return predictions;
    }

    public void setPredictions(Predictions predictions) {
        this.predictions = predictions;
    }

    public Map<String, Object> getProject_data() {
        return project_data;
    }

    public void setProject_data(Map<String, Object> project_data) {
        this.project_data = project_data;
    }

    public static class Predictions {
        private Double predicted_overrun_pct;
        private Double predicted_delay_days;
        private String cost_risk_tier;
        private String time_risk_tier;
        private String overall_risk_tier;

        public Double getPredicted_overrun_pct() {
            return predicted_overrun_pct;
        }

        public void setPredicted_overrun_pct(Double predicted_overrun_pct) {
            this.predicted_overrun_pct = predicted_overrun_pct;
        }

        public Double getPredicted_delay_days() {
            return predicted_delay_days;
        }

        public void setPredicted_delay_days(Double predicted_delay_days) {
            this.predicted_delay_days = predicted_delay_days;
        }

        public String getCost_risk_tier() {
            return cost_risk_tier;
        }

        public void setCost_risk_tier(String cost_risk_tier) {
            this.cost_risk_tier = cost_risk_tier;
        }

        public String getTime_risk_tier() {
            return time_risk_tier;
        }

        public void setTime_risk_tier(String time_risk_tier) {
            this.time_risk_tier = time_risk_tier;
        }

        public String getOverall_risk_tier() {
            return overall_risk_tier;
        }

        public void setOverall_risk_tier(String overall_risk_tier) {
            this.overall_risk_tier = overall_risk_tier;
        }
    }
}
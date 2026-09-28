package com.setu.core.e.risk.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.setu.core.c.project.entity.Project;
import com.setu.core.c.project.repository.ProjectRepository;
import com.setu.core.e.risk.client.MLServiceClient;
import com.setu.core.e.risk.dto.MLRequestDTO;
import com.setu.core.e.risk.dto.RiskScoreDTO;
import com.setu.core.e.risk.entity.RiskLevel;
import com.setu.core.e.risk.entity.RiskScore;
import com.setu.core.e.risk.repository.RiskScoreRepository;
import com.setu.core.g.alert.service.AlertService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class RiskService {

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private RiskScoreRepository riskScoreRepository;

    @Autowired
    private MLServiceClient mlServiceClient;

    @Autowired
    private AlertService alertService;

    private final ObjectMapper objectMapper = new ObjectMapper();

    // Saves what we need locally, but returns the model's response exactly as received.
    @SuppressWarnings("unchecked")
    public Map<String, Object> generateRiskScore(Long projectId) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new IllegalArgumentException("Project not found"));

        Map<String, Object> raw = mlServiceClient.getRiskPrediction(buildRequest(project));

        if (raw == null || !(raw.get("predictions") instanceof Map)) {
            throw new IllegalStateException("ML service returned no prediction");
        }
        Map<String, Object> predictions = (Map<String, Object>) raw.get("predictions");

        double overrunPct = toDouble(predictions.get("predicted_overrun_pct"));
        double delayDays = toDouble(predictions.get("predicted_delay_days"));
        String costTier = String.valueOf(predictions.get("cost_risk_tier"));
        String timeTier = String.valueOf(predictions.get("time_risk_tier"));
        String overallTier = String.valueOf(predictions.get("overall_risk_tier"));

        RiskScore riskScore = new RiskScore();
        riskScore.setProject(project);
        riskScore.setRiskScoreValue(overrunPct * 100);
        riskScore.setRiskLevel(RiskLevel.valueOf(overallTier.toUpperCase()));
        riskScore.setPredictedOverrunPct(overrunPct);
        riskScore.setPredictedDelayDays(delayDays);
        riskScore.setCostRiskLevel(RiskLevel.valueOf(costTier.toUpperCase()));
        riskScore.setTimeRiskLevel(RiskLevel.valueOf(timeTier.toUpperCase()));
        riskScore.setContributingFactors(String.format(
                "Cost risk: %s, Time risk: %s, Predicted delay: %.0f days",
                costTier, timeTier, delayDays));
        riskScore.setModelVersion("v1.0");

        try {
            riskScore.setMlProjectDataJson(objectMapper.writeValueAsString(raw.get("project_data")));
        } catch (Exception e) {
            riskScore.setMlProjectDataJson(null);
        }

        riskScoreRepository.save(riskScore);
        alertService.evaluateAndCreateAlert(project, riskScore.getRiskLevel(), riskScore.getRiskScoreValue());

        return raw;
    }

    public RiskScoreDTO getLatestRiskScore(Long projectId) {
        RiskScore riskScore = riskScoreRepository
                .findTopByProject_ProjectIdOrderByGeneratedAtDesc(projectId)
                .orElseThrow(() -> new IllegalArgumentException("No risk score found for this project"));

        return toDTO(riskScore);
    }

    private double toDouble(Object value) {
        return value instanceof Number ? ((Number) value).doubleValue() : 0.0;
    }

    private MLRequestDTO buildRequest(Project project) {
        MLRequestDTO dto = new MLRequestDTO();
        dto.setProject_name(project.getName());
        dto.setAgency(project.getImplementingAgency());
        dto.setState("N/A");
        dto.setMinistry(project.getMinistry() != null ? project.getMinistry().getName() : "N/A");
        dto.setSector(project.getSector() != null ? project.getSector().getName() : "N/A");
        dto.setStatus(project.getStatus().name());
        dto.setOriginal_cost_cr(project.getApprovedCost() != null ? project.getApprovedCost().doubleValue() : 0.0);
        dto.setCumulative_expenditure(project.getCumulativeExpenditure() != null ? project.getCumulativeExpenditure().doubleValue() : 0.0);
        dto.setPhysical_progress(project.getPhysicalProgressPercent() != null ? project.getPhysicalProgressPercent() : 0.0);
        dto.setDate_of_approval(project.getStartDate() != null ? project.getStartDate().toString() : "N/A");
        dto.setStart_date(project.getStartDate() != null ? project.getStartDate().toString() : "N/A");
        dto.setTarget_doc(project.getScheduledEndDate() != null ? project.getScheduledEndDate().toString() : "N/A");
        return dto;
    }

    private RiskScoreDTO toDTO(RiskScore riskScore) {
        return new RiskScoreDTO(
                riskScore.getProject().getProjectId(),
                riskScore.getRiskScoreValue(),
                riskScore.getRiskLevel().name(),
                riskScore.getContributingFactors(),
                riskScore.getGeneratedAt(),
                riskScore.getPredictedOverrunPct(),
                riskScore.getPredictedDelayDays(),
                riskScore.getCostRiskLevel() != null ? riskScore.getCostRiskLevel().name() : null,
                riskScore.getTimeRiskLevel() != null ? riskScore.getTimeRiskLevel().name() : null
        );
    }
}
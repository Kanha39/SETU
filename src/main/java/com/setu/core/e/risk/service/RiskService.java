package com.setu.core.e.risk.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.setu.core.c.project.entity.Project;
import com.setu.core.c.project.repository.ProjectRepository;
import com.setu.core.e.risk.client.MLServiceClient;
import com.setu.core.e.risk.dto.MLRequestDTO;
import com.setu.core.e.risk.dto.MLResponseDTO;
import com.setu.core.e.risk.dto.RiskScoreDTO;
import com.setu.core.e.risk.entity.RiskLevel;
import com.setu.core.e.risk.entity.RiskScore;
import com.setu.core.e.risk.repository.RiskScoreRepository;
import com.setu.core.g.alert.service.AlertService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

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

    public RiskScoreDTO generateRiskScore(Long projectId) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new IllegalArgumentException("Project not found"));

        MLRequestDTO request = buildRequest(project);
        MLResponseDTO response = mlServiceClient.getRiskPrediction(request);
        MLResponseDTO.Predictions predictions = response.getPredictions();

        RiskScore riskScore = new RiskScore();
        riskScore.setProject(project);
        riskScore.setRiskScoreValue(predictions.getPredicted_overrun_pct() * 100);
        riskScore.setRiskLevel(RiskLevel.valueOf(predictions.getOverall_risk_tier().toUpperCase()));
        riskScore.setPredictedOverrunPct(predictions.getPredicted_overrun_pct());
        riskScore.setPredictedDelayDays(predictions.getPredicted_delay_days());
        riskScore.setCostRiskLevel(RiskLevel.valueOf(predictions.getCost_risk_tier().toUpperCase()));
        riskScore.setTimeRiskLevel(RiskLevel.valueOf(predictions.getTime_risk_tier().toUpperCase()));
        riskScore.setContributingFactors(String.format("Cost risk: %s, Time risk: %s, Predicted delay: %.0f days",
                predictions.getCost_risk_tier(), predictions.getTime_risk_tier(), predictions.getPredicted_delay_days()));
        riskScore.setModelVersion("v1.0");

        try {
            riskScore.setMlProjectDataJson(objectMapper.writeValueAsString(response.getProject_data()));
        } catch (Exception e) {
            riskScore.setMlProjectDataJson(null);
        }

        RiskScore saved = riskScoreRepository.save(riskScore);
        alertService.evaluateAndCreateAlert(project, riskScore.getRiskLevel(), riskScore.getRiskScoreValue());

        return toDTO(saved);
    }

    public RiskScoreDTO getLatestRiskScore(Long projectId) {
        RiskScore riskScore = riskScoreRepository
                .findTopByProject_ProjectIdOrderByGeneratedAtDesc(projectId)
                .orElseThrow(() -> new IllegalArgumentException("No risk score found for this project"));

        return toDTO(riskScore);
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
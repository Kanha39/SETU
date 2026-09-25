package com.setu.core.d.mitigation.service;

import com.setu.core.d.mitigation.client.MitigationServiceClient;
import com.setu.core.d.mitigation.dto.*;
import com.setu.core.d.mitigation.entity.MitigationStrategy;
import com.setu.core.d.mitigation.entity.QuestionnaireResponse;
import com.setu.core.d.mitigation.repository.MitigationStrategyRepository;
import com.setu.core.d.mitigation.repository.QuestionnaireResponseRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MitigationService {

    @Autowired
    private QuestionnaireResponseRepository questionnaireRepository;

    @Autowired
    private MitigationStrategyRepository strategyRepository;

    @Autowired
    private MitigationServiceClient mitigationServiceClient;

    public QuestionnaireResponseDTO submitQuestionnaire(QuestionnaireSubmitDTO dto) {
        int nextSessionId = questionnaireRepository
                .findTopByProjectNameOrderBySessionIdDesc(dto.getProjectName())
                .map(r -> r.getSessionId() + 1)
                .orElse(1);

        QuestionnaireResponse response = new QuestionnaireResponse();
        response.setProjectName(dto.getProjectName());
        response.setSessionId(nextSessionId);
        response.setLandAcquisition(dto.getLandAcquisition());
        response.setFinancialResult(dto.getFinancialResult());
        response.setApprovalClearance(dto.getApprovalClearance());
        response.setScopeDesign(dto.getScopeDesign());
        response.setProcurementResult(dto.getProcurementResult());
        response.setExecutionPace(dto.getExecutionPace());
        response.setInteragencyCoordination(dto.getInteragencyCoordination());

        questionnaireRepository.save(response);

        return new QuestionnaireResponseDTO(dto.getProjectName(), nextSessionId);
    }

    public MitigationStrategyDTO generateMitigationStrategy(MitigationRequestDTO dto) {
        QuestionnaireResponse questionnaire = questionnaireRepository
                .findByProjectNameAndSessionId(dto.getProjectName(), dto.getSessionId())
                .orElseThrow(() -> new IllegalArgumentException(
                        "No questionnaire found for this project and session"));

        int nextStrategyId = strategyRepository
                .findTopByProjectNameAndSessionIdOrderByStrategyIdDesc(dto.getProjectName(), dto.getSessionId())
                .map(s -> s.getStrategyId() + 1)
                .orElse(1);

        ExternalMitigationRequestDTO request = new ExternalMitigationRequestDTO();
        request.setSession_id(String.valueOf(dto.getSessionId()));
        request.setProject_name(questionnaire.getProjectName());
        request.setLand_acquisition(questionnaire.getLandAcquisition());
        request.setFinancial_result(questionnaire.getFinancialResult());
        request.setApproval_clearance(questionnaire.getApprovalClearance());
        request.setProcurement_result(questionnaire.getProcurementResult());
        request.setScope_design(questionnaire.getScopeDesign());
        request.setExecution_pace(questionnaire.getExecutionPace());
        request.setInteragency_coordination(questionnaire.getInteragencyCoordination());
        request.setCreated_at(questionnaire.getCreatedAt().toString());

        String answer = mitigationServiceClient.getMitigationStrategy(request);

        MitigationStrategy strategy = new MitigationStrategy();
        strategy.setProjectName(dto.getProjectName());
        strategy.setSessionId(dto.getSessionId());
        strategy.setStrategyId(nextStrategyId);
        strategy.setMitigationStrategy(answer);

        MitigationStrategy saved = strategyRepository.save(strategy);

        return toDTO(saved);
    }

    public List<MitigationStrategyDTO> getStrategyHistory(String projectName, Integer sessionId) {
        return strategyRepository
                .findByProjectNameAndSessionIdOrderByStrategyIdAsc(projectName, sessionId)
                .stream()
                .map(this::toDTO)
                .toList();
    }

    private MitigationStrategyDTO toDTO(MitigationStrategy s) {
        return new MitigationStrategyDTO(
                s.getProjectName(), s.getSessionId(), s.getStrategyId(),
                s.getMitigationStrategy(), s.getCreatedAt()
        );
    }
}
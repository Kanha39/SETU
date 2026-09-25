package com.setu.core.d.mitigation.controller;

import com.setu.core.d.mitigation.dto.*;
//import com.setu.core.d.mitigation.dto.MitigationRequestDTO;
import com.setu.core.d.mitigation.service.MitigationService;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/mitigation")
public class MitigationController {

    @Autowired
    private MitigationService mitigationService;

    @PostMapping("/questionnaire")
    public ResponseEntity<QuestionnaireResponseDTO> submitQuestionnaire(
            @Valid @RequestBody QuestionnaireSubmitDTO dto) {
        return ResponseEntity.ok(mitigationService.submitQuestionnaire(dto));
    }

    @PostMapping("/generate")
    public ResponseEntity<MitigationStrategyDTO> generate(@Valid @RequestBody MitigationRequestDTO dto) {
        return ResponseEntity.ok(mitigationService.generateMitigationStrategy(dto));
    }

    @GetMapping("/{projectName}/{sessionId}/strategies")
    public ResponseEntity<List<MitigationStrategyDTO>> getStrategies(
            @PathVariable String projectName, @PathVariable Integer sessionId) {
        return ResponseEntity.ok(mitigationService.getStrategyHistory(projectName, sessionId));
    }
}
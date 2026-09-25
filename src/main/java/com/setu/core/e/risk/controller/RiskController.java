package com.setu.core.e.risk.controller;

import com.setu.core.e.risk.dto.RiskScoreDTO;
import com.setu.core.e.risk.service.RiskService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/projects/{projectId}/risk")
public class RiskController {

    @Autowired
    private RiskService riskService;

    @PostMapping("/generate")
    public ResponseEntity<RiskScoreDTO> generate(@PathVariable Long projectId) {
        return ResponseEntity.ok(riskService.generateRiskScore(projectId));
    }

    @GetMapping("/latest")
    public ResponseEntity<RiskScoreDTO> getLatest(@PathVariable Long projectId) {
        return ResponseEntity.ok(riskService.getLatestRiskScore(projectId));
    }
}
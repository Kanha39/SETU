package com.setu.core.g.alert.controller;

import com.setu.core.g.alert.dto.AlertDto;
import com.setu.core.g.alert.service.AlertService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/alerts")
public class AlertController {

    @Autowired
    private AlertService alertService;

    @GetMapping
    public ResponseEntity<List<AlertDto>> getActiveAlerts() {
        return ResponseEntity.ok(alertService.getActiveAlerts());
    }

    @PostMapping("/{alertId}/acknowledge")
    public ResponseEntity<AlertDto> acknowledge(@PathVariable Long alertId) {
        return ResponseEntity.ok(alertService.acknowledgeAlert(alertId));
    }
}
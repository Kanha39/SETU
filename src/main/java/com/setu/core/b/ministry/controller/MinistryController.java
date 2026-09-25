package com.setu.core.b.ministry.controller;

import com.setu.core.b.ministry.dto.SectorDto;
import com.setu.core.b.ministry.service.MinistryService;
import com.setu.core.b.ministry.dto.MinistryDto;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class MinistryController {

    @Autowired
    private MinistryService ministryService;

    @PostMapping("/ministries")
    public ResponseEntity<MinistryDto> createMinistry(@Valid @RequestBody MinistryDto dto) {
        return ResponseEntity.ok(ministryService.createMinistry(dto));
    }

    @GetMapping("/ministries")
    public ResponseEntity<List<MinistryDto>> getAllMinistries() {
        return ResponseEntity.ok(ministryService.getAllMinistries());
    }

    @PostMapping("/sectors")
    public ResponseEntity<SectorDto> createSector(@Valid @RequestBody SectorDto dto) {
        return ResponseEntity.ok(ministryService.createSector(dto));
    }

    @GetMapping("/sectors")
    public ResponseEntity<List<SectorDto>> getAllSectors() {
        return ResponseEntity.ok(ministryService.getAllSectors());
    }
}
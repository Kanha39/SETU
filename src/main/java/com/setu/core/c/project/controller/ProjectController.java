package com.setu.core.c.project.controller;

import com.setu.core.c.project.dto.ProjectRequestDTO;
import com.setu.core.c.project.dto.ProjectResponseDTO;
import com.setu.core.c.project.entity.ProjectStatus;
import com.setu.core.c.project.service.ProjectService;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/projects")
public class ProjectController {

    @Autowired
    private ProjectService projectService;

    @PostMapping
    public ResponseEntity<ProjectResponseDTO> create(@Valid @RequestBody ProjectRequestDTO dto) {
        return ResponseEntity.ok(projectService.createProject(dto));
    }

    @PutMapping("/{projectId}")
    public ResponseEntity<ProjectResponseDTO> update(@PathVariable Long projectId,
                                                     @Valid @RequestBody ProjectRequestDTO dto) {
        return ResponseEntity.ok(projectService.updateProject(projectId, dto));
    }

    @GetMapping("/{projectId}")
    public ResponseEntity<ProjectResponseDTO> get(@PathVariable Long projectId) {
        return ResponseEntity.ok(projectService.getProject(projectId));
    }

    @GetMapping
    public ResponseEntity<List<ProjectResponseDTO>> getAll(
            @RequestParam(required = false) ProjectStatus status) {
        if (status != null) {
            return ResponseEntity.ok(projectService.getProjectsByStatus(status));
        }
        return ResponseEntity.ok(projectService.getAllProjects());
    }
}
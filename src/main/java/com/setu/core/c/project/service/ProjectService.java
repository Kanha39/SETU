package com.setu.core.c.project.service;

import com.setu.core.b.ministry.entity.Ministry;
import com.setu.core.b.ministry.entity.Sector;
import com.setu.core.b.ministry.repository.MinistryRepository;
import com.setu.core.b.ministry.repository.SectorRepository;
import com.setu.core.c.project.dto.ProjectRequestDTO;
import com.setu.core.c.project.dto.ProjectResponseDTO;
import com.setu.core.c.project.entity.Project;
import com.setu.core.c.project.entity.ProjectStatus;
import com.setu.core.c.project.repository.ProjectRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class ProjectService {

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private MinistryRepository ministryRepository;

    @Autowired
    private SectorRepository sectorRepository;

    public ProjectResponseDTO createProject(ProjectRequestDTO dto) {
        Project project = new Project();
        applyDTO(project, dto);
        project.setStatus(ProjectStatus.ON_TRACK);

        return toResponseDTO(projectRepository.save(project));
    }

    public ProjectResponseDTO updateProject(Long projectId, ProjectRequestDTO dto) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new IllegalArgumentException("Project not found"));

        applyDTO(project, dto);

        return toResponseDTO(projectRepository.save(project));
    }

    public ProjectResponseDTO getProject(Long projectId) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new IllegalArgumentException("Project not found"));

        return toResponseDTO(project);
    }

    public List<ProjectResponseDTO> getAllProjects() {
        return projectRepository.findAll()
                .stream()
                .map(this::toResponseDTO)
                .collect(Collectors.toList());
    }

    public List<ProjectResponseDTO> getProjectsByStatus(ProjectStatus status) {
        return projectRepository.findByStatus(status)
                .stream()
                .map(this::toResponseDTO)
                .collect(Collectors.toList());
    }

    private void applyDTO(Project project, ProjectRequestDTO dto) {
        project.setName(dto.getName());
        project.setImplementingAgency(dto.getImplementingAgency());
        project.setApprovedCost(dto.getApprovedCost());
        project.setRevisedCost(dto.getRevisedCost());
        project.setCumulativeExpenditure(dto.getCumulativeExpenditure());
        project.setStartDate(dto.getStartDate());
        project.setScheduledEndDate(dto.getScheduledEndDate());
        project.setRevisedEndDate(dto.getRevisedEndDate());
        project.setPhysicalProgressPercent(dto.getPhysicalProgressPercent());

        if (dto.getMinistryId() != null) {
            Ministry ministry = ministryRepository.findById(dto.getMinistryId())
                    .orElseThrow(() -> new IllegalArgumentException("Ministry not found"));
            project.setMinistry(ministry);
        }

        if (dto.getSectorId() != null) {
            Sector sector = sectorRepository.findById(dto.getSectorId())
                    .orElseThrow(() -> new IllegalArgumentException("Sector not found"));
            project.setSector(sector);
        }
    }

    private ProjectResponseDTO toResponseDTO(Project project) {
        return new ProjectResponseDTO(
                project.getProjectId(),
                project.getName(),
                project.getMinistry() != null ? project.getMinistry().getName() : null,
                project.getSector() != null ? project.getSector().getName() : null,
                project.getImplementingAgency(),
                project.getApprovedCost(),
                project.getRevisedCost(),
                project.getCumulativeExpenditure(),
                project.getStartDate(),
                project.getScheduledEndDate(),
                project.getRevisedEndDate(),
                project.getPhysicalProgressPercent(),
                project.getStatus().name(),
                project.getLastUpdated()
        );
    }
}
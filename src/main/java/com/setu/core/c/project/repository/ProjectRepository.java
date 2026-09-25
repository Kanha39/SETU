package com.setu.core.c.project.repository;

import com.setu.core.c.project.entity.Project;
import com.setu.core.c.project.entity.ProjectStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ProjectRepository extends JpaRepository<Project, Long> {
    List<Project> findByStatus(ProjectStatus status);
    List<Project> findByMinistry_MinistryId(Long ministryId);
}
package com.setu.core.d.mitigation.repository;

import com.setu.core.d.mitigation.entity.QuestionnaireResponse;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

public interface QuestionnaireResponseRepository extends JpaRepository<QuestionnaireResponse, Long> {
    Optional<QuestionnaireResponse> findTopByProjectNameOrderBySessionIdDesc(String projectName);
    Optional<QuestionnaireResponse> findByProjectNameAndSessionId(String projectName, Integer sessionId);
    List<QuestionnaireResponse> findByProjectNameOrderBySessionIdAsc(String projectName);
}
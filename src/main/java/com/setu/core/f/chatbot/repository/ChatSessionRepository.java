package com.setu.core.f.chatbot.repository;

import com.setu.core.f.chatbot.entity.ChatSession;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ChatSessionRepository extends JpaRepository<ChatSession, Long> {
    List<ChatSession> findByUser_UserIdOrderByLastMessageAtDesc(Long userId);
}
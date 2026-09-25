package com.setu.core.f.chatbot.client;

import com.setu.core.f.chatbot.dto.ExternalChatRequestDTO;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Component
public class ChatbotServiceClient {

    private final WebClient webClient;

    public ChatbotServiceClient(WebClient.Builder webClientBuilder,
                                @Value("${chatbot.service.base-url}") String chatbotBaseUrl) {
        HttpClient httpClient = HttpClient.create()
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 15000)
                .responseTimeout(Duration.ofSeconds(60))
                .doOnConnected(conn -> conn
                        .addHandlerLast(new ReadTimeoutHandler(60, TimeUnit.SECONDS)));

        this.webClient = webClientBuilder
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .baseUrl(chatbotBaseUrl)
                .build();
    }

    public String getAnswer(Long sessionId, String message, Map<String, Object> userProject, List<Map<String, String>> history) {
        ExternalChatRequestDTO request = new ExternalChatRequestDTO();
        request.setSession_id(sessionId != null ? sessionId.toString() : null);
        request.setMessage(message);
        request.setUser_project(userProject);
        request.setHistory(history);

        try {
            System.out.println("SENDING TO CHATBOT: " + new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(request));

            Map response = webClient.post()
                    .uri("/api/chat")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            return response != null && response.get("answer") != null
                    ? response.get("answer").toString()
                    : "Sorry, I couldn't process that.";
        } catch (org.springframework.web.reactive.function.client.WebClientResponseException e) {
            System.out.println("CHATBOT CALL FAILED: " + e.getStatusCode() + " - " + e.getResponseBodyAsString());
            return "The chatbot service is currently unavailable. Please try again shortly.";
        } catch (Exception e) {
            System.out.println("CHATBOT CALL FAILED: " + e.getClass().getName() + " - " + e.getMessage());
            return "The chatbot service is currently unavailable. Please try again shortly.";
        }
    }
}
package com.setu.core.d.mitigation.client;

import com.setu.core.d.mitigation.dto.ExternalMitigationRequestDTO;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Component
public class MitigationServiceClient {

    private final WebClient webClient;

    public MitigationServiceClient(WebClient.Builder webClientBuilder,
                                   @Value("${chatbot.service.base-url}") String baseUrl) {
        HttpClient httpClient = HttpClient.create()
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 15000)
                .responseTimeout(Duration.ofSeconds(60))
                .doOnConnected(conn -> conn
                        .addHandlerLast(new ReadTimeoutHandler(60, TimeUnit.SECONDS)));

        this.webClient = webClientBuilder
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .baseUrl(baseUrl)
                .build();
    }

    public String getMitigationStrategy(ExternalMitigationRequestDTO request) {
        try {
            System.out.println("SENDING TO /api/project/mitigation: "
                    + new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(request));

            Map response = webClient.post()
                    .uri("/api/project/mitigation")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            System.out.println("MITIGATION RESPONSE: " + response);

            if (response == null) return "Sorry, I couldn't process that.";

            // TODO: confirm exact response key once seen — trying common candidates
            for (String key : new String[]{"mitigation_strategy", "strategy", "answer", "result"}) {
                if (response.get(key) != null) return response.get(key).toString();
            }
            return response.toString(); // fallback: show whatever came back, for debugging

        } catch (org.springframework.web.reactive.function.client.WebClientResponseException e) {
            System.out.println("MITIGATION CALL FAILED: " + e.getStatusCode() + " - " + e.getResponseBodyAsString());
            return "The mitigation service is currently unavailable. Please try again shortly.";
        } catch (Exception e) {
            System.out.println("MITIGATION CALL FAILED: " + e.getClass().getName() + " - " + e.getMessage());
            return "The mitigation service is currently unavailable. Please try again shortly.";
        }
    }
}
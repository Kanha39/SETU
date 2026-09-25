package com.setu.core.e.risk.client;

import com.setu.core.e.risk.dto.MLRequestDTO;
import com.setu.core.e.risk.dto.MLResponseDTO;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class MLServiceClient {

    private final WebClient webClient;

    public MLServiceClient(WebClient.Builder webClientBuilder,
                           @Value("${ml.service.base-url}") String mlServiceBaseUrl) {
        this.webClient = webClientBuilder.baseUrl(mlServiceBaseUrl).build();
    }

    public MLResponseDTO getRiskPrediction(MLRequestDTO request) {
        return webClient.post()
                .uri("api//predict")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(MLResponseDTO.class)
                .block();   // synchronous call — fine for now, revisit if you add reactive controllers later
    }
}
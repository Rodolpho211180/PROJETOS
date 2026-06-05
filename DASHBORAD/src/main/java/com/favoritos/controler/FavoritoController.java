package com.favoritos.controller;

import com.favoritos.model.Favorito;
import com.favoritos.service.FavoritoService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/favoritos")
@CrossOrigin
public class FavoritoController {

    private final FavoritoService service;

    public FavoritoController(FavoritoService service) {
        this.service = service;
    }

    @GetMapping
    public List<Favorito> listar() {
        return service.listar();
    }

    @PostMapping
    public Favorito adicionar(@RequestBody Favorito favorito) {
        return service.adicionar(favorito);
    }

    @DeleteMapping("/{id}")
    public void remover(@PathVariable Long id) {
        service.remover(id);
    }
}
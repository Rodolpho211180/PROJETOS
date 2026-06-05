package com.favoritos.service;

import com.favoritos.model.Favorito;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class FavoritoService {

    private final List<Favorito> favoritos = new ArrayList<>();

    public List<Favorito> listar() {
        return favoritos;
    }

    public Favorito adicionar(Favorito favorito) {
        favorito.setId((long) (favoritos.size() + 1));
        favoritos.add(favorito);
        return favorito;
    }

    public void remover(Long id) {
        favoritos.removeIf(f -> f.getId().equals(id));
    }
}
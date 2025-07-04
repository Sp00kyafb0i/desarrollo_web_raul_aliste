package tarea4.webdev.tarea4.controller;

import tarea4.webdev.tarea4.model.Actividad;
import tarea4.webdev.tarea4.model.Nota;
import tarea4.webdev.tarea4.repository.ActividadRepository;
import tarea4.webdev.tarea4.repository.NotaRepository;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api")
public class NotaController {

    private final NotaRepository notaRepo;
    private final ActividadRepository actividadRepo;

    public NotaController(NotaRepository notaRepo, ActividadRepository actividadRepo) {
        this.notaRepo = notaRepo;
        this.actividadRepo = actividadRepo;
    }

    @GetMapping("/actividades")
    public List<Map<String, Object>> getActividadesPasadas() {
        LocalDateTime ahora = LocalDateTime.now();
        return actividadRepo.findByDiaHoraTerminoBefore(ahora).stream().map(act -> {
            Map<String, Object> obj = new HashMap<>();
            obj.put("id", act.getId());
            obj.put("fechaInicio", act.getDiaHoraInicio());
            obj.put("sector", act.getSector());
            obj.put("nombre", act.getNombre());
            obj.put("tema", act.getDescripcion()); // usando descripción como tema
            List<Nota> notas = notaRepo.findByActividadId(act.getId());
            obj.put("notaPromedio", notas.isEmpty() ? null :
                notas.stream().mapToInt(Nota::getNota).average().orElse(0));
            return obj;
        }).collect(Collectors.toList());
    }

    @PostMapping("/nota")
    public Map<String, Object> agregarNota(@RequestParam Integer actividadId, @RequestParam Integer nota) {
        if (nota < 1 || nota > 7) throw new IllegalArgumentException("Nota inválida");
        Nota nueva = new Nota();
        nueva.setNota(nota);
        nueva.setActividad(actividadRepo.findById(actividadId).orElseThrow());
        notaRepo.save(nueva);
        List<Nota> notas = notaRepo.findByActividadId(actividadId);
        double promedio = notas.stream().mapToInt(Nota::getNota).average().orElse(0);
        return Map.of("success", true, "nuevoPromedio", promedio);
    }
}




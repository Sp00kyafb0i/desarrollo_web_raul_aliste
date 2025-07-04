package tarea4.webdev.tarea4.repository;

import tarea4.webdev.tarea4.model.Actividad;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface ActividadRepository extends JpaRepository<Actividad, Integer> {
    List<Actividad> findByDiaHoraTerminoBefore(LocalDateTime fechaHora);
}

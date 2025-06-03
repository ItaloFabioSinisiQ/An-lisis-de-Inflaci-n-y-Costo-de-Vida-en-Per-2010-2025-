# 📊 Documentación Técnica: Dashboard de Análisis Económico del Perú

## 🎯 Descripción General

Dashboard interactivo desarrollado en HTML/CSS/JavaScript que presenta un análisis exploratorio completo sobre la evolución de la inflación y el costo de vida en Perú durante el período 2010-2024. Utiliza datos oficiales del INEI (Instituto Nacional de Estadística e Informática) y BCRP (Banco Central de Reserva del Perú).

---

## 🏗️ Arquitectura Técnica

### Tecnologías Utilizadas
- **HTML5**: Estructura semántica del dashboard
- **CSS3**: Estilos avanzados con gradientes, efectos glassmorphism y animaciones
- **JavaScript ES6+**: Lógica de negocio y manipulación del DOM
- **Chart.js v3.9.1**: Librería de visualización de datos
- **Papa Parse v5.4.1**: Procesamiento de archivos CSV (preparado para uso futuro)

### Arquitectura de Componentes
```
Dashboard/
├── Header (Título y descripción)
├── Summary Stats (6 tarjetas de métricas clave)
├── Dashboard Grid (6 gráficos principales)
│   ├── IPC Chart (Inflación)
│   ├── Canasta Chart (Costo de vida)
│   ├── RMV vs Canasta Chart (Comparativo)
│   ├── Pobreza Chart (Indicadores sociales)
│   ├── Tipo Cambio Chart (USD/PEN)
│   └── Deciles Chart (Distribución ingresos)
└── Analysis Section (Insights y conclusiones)
```

---

## 📈 Fuentes de Datos

### Datasets Integrados

1. **IPC (Índice de Precios al Consumidor)**
   - Período: 2010-2024
   - Frecuencia: Anual
   - Fuente: INEI
   - Formato: Porcentaje de variación anual

2. **Canasta Básica Familiar**
   - Componentes: Alimentaria y Total
   - Unidad: Soles per cápita mensual
   - Período: 2010-2024
   - Fuente: INEI

3. **Remuneración Mínima Vital (RMV)**
   - Histórico de ajustes desde 2010
   - Valor actual: S/ 1,130 (Enero 2025)
   - Fuente: MTPE

4. **Tasas de Pobreza**
   - Pobreza monetaria y extrema
   - Cobertura: Nacional
   - Período: 2010-2023
   - Fuente: INEI

5. **Tipo de Cambio USD/PEN**
   - Valores de cierre anual
   - Período: 2010-2025
   - Fuente: BCRP

6. **Distribución de Ingresos por Deciles**
   - Año de referencia: 2023
   - Unidad: Soles mensuales
   - Fuente: INEI - ENAHO

---

## 🛠️ Estructura del Código

### Configuración Global
```javascript
// Configuración Chart.js
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#2c3e50';
```

### Objeto de Datos Principal
```javascript
const data = {
    ipc: [...],           // Datos de inflación
    canasta: [...],       // Canasta básica familiar
    rmv: [...],           // Remuneración mínima vital
    pobreza: [...],       // Tasas de pobreza
    tipoCambio: [...],    // Tipo de cambio
    deciles2023: [...]    // Distribución de ingresos
};
```

### Funciones Principales

#### 1. `createSummaryStats()`
- **Propósito**: Genera las 6 tarjetas de estadísticas resumen
- **Cálculos**: Promedios, máximos, valores actuales
- **Salida**: HTML dinámico insertado en el DOM

#### 2. `createIPCChart()`
- **Tipo**: Gráfico de línea con área rellena
- **Datos**: Variación anual del IPC
- **Características**: Puntos destacados, gradiente de fondo
- **Configuración**: Escala Y desde 0, etiquetas personalizadas

#### 3. `createCanastaChart()`
- **Tipo**: Gráfico de línea múltiple
- **Series**: Canasta alimentaria y total
- **Visualización**: Comparativa de evolución temporal
- **Colores**: Naranja (#f39c12) y Azul (#3498db)

#### 4. `createRMVCanastaChart()`
- **Propósito**: Comparar RMV vs costo familiar
- **Cálculo especial**: Canasta familiar = Canasta per cápita × 4
- **Interpolación**: RMV por períodos de vigencia
- **Insight**: Visualiza la brecha de cobertura

#### 5. `createPobrezaChart()`
- **Series**: Pobreza monetaria y extrema
- **Período crítico**: Destaca impacto COVID-19 (2020)
- **Escala**: 0-35% para mejor visualización
- **Colores**: Rojo (#e74c3c) y Violeta (#8e44ad)

#### 6. `createTipoCambioChart()`
- **Rango**: 2.5-4.0 soles por dólar
- **Propósito**: Monitorear volatilidad cambiaria
- **Indicador**: Presiones inflacionarias importadas

#### 7. `createDecilesChart()`
- **Tipo**: Gráfico de barras
- **Datos**: Ingresos por decil poblacional
- **Colores**: Gradiente de 10 colores únicos
- **Insight**: Visualiza desigualdad de ingresos

---

## 🎨 Sistema de Diseño

### Paleta de Colores
```css
/* Colores principales */
--primary-blue: #3498db
--danger-red: #e74c3c
--success-green: #27ae60
--warning-orange: #f39c12
--dark-blue: #2c3e50
--purple: #8e44ad

/* Fondo */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
```

### Efectos Visuales
- **Glassmorphism**: `backdrop-filter: blur(10px)`
- **Sombras**: `box-shadow: 0 10px 30px rgba(0,0,0,0.1)`
- **Transiciones**: `transition: transform 0.3s ease`
- **Hover Effects**: `transform: translateY(-5px)`

### Responsividad
```css
.dashboard {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
}
```

---

## 📱 Compatibilidad

### Navegadores Soportados
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Dispositivos
- **Desktop**: Resoluciones 1024px+
- **Tablet**: 768px - 1023px
- **Mobile**: 320px - 767px (diseño adaptativo)

---

## 🚀 Guía de Implementación

### 1. Estructura de Archivos
```
proyecto/
├── index.html (dashboard completo)
├── data/ (opcional para CSVs externos)
│   ├── canasta_basica.csv
│   ├── ipc_data.csv
│   └── pobreza_data.csv
└── README.md
```

### 2. Dependencias CDN
```html
<!-- Chart.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>

<!-- Papa Parse (opcional) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/papaparse/5.4.1/papaparse.min.js"></script>
```

### 3. Inicialización
```javascript
document.addEventListener('DOMContentLoaded', function() {
    createSummaryStats();
    createIPCChart();
    createCanastaChart();
    createRMVCanastaChart();
    createPobrezaChart();
    createTipoCambioChart();
    createDecilesChart();
});
```

---

## 🔧 Personalización y Extensiones

### Añadir Nuevos Gráficos
1. Crear función `createNuevoChart()`
2. Añadir canvas en HTML: `<canvas id="nuevoChart"></canvas>`
3. Incluir datos en objeto `data`
4. Llamar función en `DOMContentLoaded`

### Modificar Datos
```javascript
// Ejemplo: Actualizar datos de inflación
data.ipc.push({año: 2025, valor: 2.5});

// Recrear gráfico
createIPCChart();
```

### Añadir Interactividad
```javascript
// Ejemplo: Filtros por período
function filterByYear(startYear, endYear) {
    const filteredData = data.ipc.filter(item => 
        item.año >= startYear && item.año <= endYear
    );
    // Actualizar gráfico con datos filtrados
}
```

---

## 📊 Métricas y KPIs

### Estadísticas Calculadas
- **IPC Promedio**: Media aritmética 2010-2024
- **Inflación Máxima**: Valor pico del período
- **Brecha RMV-Canasta**: Diferencia porcentual
- **Ratio Desigualdad**: D10/D1 de ingresos
- **Tendencia Pobreza**: Variación quinquenal

### Fórmulas Implementadas
```javascript
// Promedio IPC
const ipcPromedio = data.ipc.reduce((sum, item) => sum + item.valor, 0) / data.ipc.length;

// Canasta familiar (4 personas)
const canastaFamiliar = canastaPerCapita * 4;

// Ratio desigualdad
const ratioDesigualdad = deciles[9] / deciles[0]; // D10/D1
```

---

## ⚠️ Consideraciones Técnicas

### Limitaciones
- **Datos estáticos**: Información embebida en JavaScript
- **Sin backend**: No hay persistencia de datos
- **Responsividad**: Optimizado para pantallas 350px+
- **Idioma**: Interfaz en español únicamente

### Optimizaciones Implementadas
- **Lazy loading**: Gráficos se crean bajo demanda
- **CSS optimizado**: Uso de `transform` para animaciones
- **Chart.js optimizado**: Configuración `maintainAspectRatio: false`

### Seguridad
- **CDN confiables**: Uso de cdnjs.cloudflare.com
- **No localStorage**: Sin almacenamiento local por restricciones
- **Sanitización**: Datos numéricos validados

---

## 🔍 Análisis e Insights Integrados

### Insights Automáticos Generados

1. **Crisis Inflacionaria 2021-2022**
   - Detección automática de picos inflacionarios
   - Correlación con eventos sociopolíticos

2. **Brecha Socioeconómica**
   - Cálculo automático RMV vs Canasta familiar
   - Identificación de períodos críticos

3. **Impacto Pandemia**
   - Análisis de anomalías 2020-2021
   - Efectos en indicadores de pobreza

4. **Recuperación Económica**
   - Tendencias de estabilización 2023-2024
   - Proyecciones implícitas

---

## 📝 Mantenimiento y Actualizaciones

### Frecuencia de Actualización Recomendada
- **Datos IPC**: Mensual (INEI)
- **Canasta Básica**: Trimestral (INEI)
- **RMV**: Por decreto gubernamental
- **Pobreza**: Anual (ENAHO-INEI)
- **Tipo Cambio**: Diario (BCRP)

### Procedimiento de Actualización
1. Obtener datos oficiales de fuentes
2. Validar formato y consistencia
3. Actualizar objeto `data` en JavaScript
4. Verificar visualizaciones
5. Actualizar análisis de insights

---

## 🤝 Contribuciones y Soporte

### Estructura para Contribuciones
- Seguir estándares ES6+
- Documentar nuevas funciones
- Mantener consistencia visual
- Validar datos antes de integrar

### Contacto Técnico
Para consultas técnicas o mejoras al dashboard, documentar issues con:
- Descripción del problema/mejora
- Datos de reproducción
- Propuesta de solución
- Screenshots (si aplica)

---

## 📄 Licencia y Atribuciones

### Datos
- **INEI**: Instituto Nacional de Estadística e Informática del Perú
- **BCRP**: Banco Central de Reserva del Perú
- **MTPE**: Ministerio de Trabajo y Promoción del Empleo

### Librerías
- **Chart.js**: MIT License
- **Papa Parse**: MIT License

### Código
Dashboard desarrollado como herramienta de análisis económico educativo y de investigación.

---

*Última actualización: Junio 2025 | Versión: 1.0*

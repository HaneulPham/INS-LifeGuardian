package health;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Random;
import java.util.UUID;

public class HealthDataGeneratorAll {
    private static final Random RANDOM = new Random();

    /**
     * Uses HealthDataInputConfig as class-based input and generates JSON files into this folder.
     */
    public static void main(String[] args) throws IOException {
        HealthDataInput input = HealthDataInputConfig.input();
        generateFiles(input, Path.of("."));
    }

    /**
     * Generates one file for a single health type, or all files when healthType is ALL.
     */
    public static void generateFiles(HealthDataInput input, Path outputFolder) throws IOException {
        Files.createDirectories(outputFolder);

        if (input.healthType == HealthType.ALL) {
            for (HealthType type : HealthType.values()) {
                if (type != HealthType.ALL) {
                    generateOneFile(input.withHealthType(type), outputFolder);
                }
            }
            return;
        }

        generateOneFile(input, outputFolder);
    }

    /**
     * Writes one generated Bundle to the correct JSON file name.
     */
    private static void generateOneFile(HealthDataInput input, Path outputFolder) throws IOException {
        Path outputPath = outputFolder.resolve(fileNameFor(input.healthType));
        Files.writeString(outputPath, toJson(generateBundle(input), 0));
        System.out.println("Saved " + input.healthType + " to " + outputPath);
    }

    /**
     * Builds a FHIR batch Bundle containing observations for the requested dates.
     */
    private static Map<String, Object> generateBundle(HealthDataInput input) {
        Map<String, Object> bundle = object();
        bundle.put("resourceType", "Bundle");
        bundle.put("type", "batch");

        List<Object> entries = new ArrayList<>();
        input.startDate.datesUntil(input.endDate.plusDays(1)).forEach(date -> addObservationsForDate(entries, date, input));

        bundle.put("entry", entries);
        return bundle;
    }

    /**
     * Adds all observations for one date based on the selected health type.
     */
    private static void addObservationsForDate(List<Object> entries, LocalDate date, HealthDataInput input) {
        switch (input.healthType) {
            case ALL:
                throw new IllegalArgumentException("Use generateFiles for HealthType.ALL");
            case BLOOD_GLUCOSE:
                repeat(input.count, () -> entries.add(entry(quantityObservation(
                        "15074-8",
                        "Glucose [Moles/volume] in Blood",
                        "HKQuantityTypeIdentifierBloodGlucose",
                        "Blood Glucose",
                        "laboratory",
                        randomTime(date, 6, 22),
                        null,
                        round(randomInRange(input.range(RangeKey.BLOOD_GLUCOSE, 4.1, 7.9)), 1),
                        "mmol/L",
                        "mmol/L",
                        input
                ))));
                break;
            case BLOOD_PRESSURE:
                repeat(input.count, () -> addBloodPressure(entries, date, input));
                break;
            case ECG:
                repeat(input.count, () -> entries.add(entry(ecgObservation(date, input))));
                break;
            case INR:
                repeat(input.count, () -> entries.add(entry(quantityObservation(
                        "34714-6",
                        "INR in Blood by Coagulation assay",
                        null,
                        null,
                        "vital-signs",
                        randomTime(date, 8, 12),
                        null,
                        round(randomInRange(input.range(RangeKey.INR, 1.9, 3.1)), 1),
                        null,
                        null,
                        input
                ))));
                break;
            case PULSE:
                repeat(input.count, () -> entries.add(entry(quantityObservation(
                        "8867-4",
                        "Heart rate",
                        "HKQuantityTypeIdentifierHeartRate",
                        "Heart Rate",
                        "vital-signs",
                        randomTime(date, 7, 22),
                        null,
                        Math.round(randomInRange(input.range(RangeKey.PULSE, 50, 120))),
                        "/min",
                        "beats/minute",
                        input
                ))));
                break;
            case RESPIRATORY_RATE:
                repeat(input.count, () -> entries.add(entry(quantityObservation(
                        "9279-1",
                        "Respiratory rate",
                        "HKQuantityTypeIdentifierRespiratoryRate",
                        "Respiratory Rate",
                        "vital-signs",
                        randomTime(date, 7, 22),
                        null,
                        Math.round(randomInRange(input.range(RangeKey.RESPIRATORY_RATE, 10, 25))),
                        "/min",
                        "breaths/minute",
                        input
                ))));
                break;
            case SLEEP:
                for (Map<String, Object> observation : sleepObservations(date, input)) {
                    entries.add(entry(observation));
                }
                break;
            case SPO2:
                repeat(input.count, () -> entries.add(entry(quantityObservation(
                        "59408-5",
                        "Oxygen saturation in Arterial blood by Pulse oximetry",
                        "HKQuantityTypeIdentifierOxygenSaturation",
                        "Oxygen Saturation (SpO2)",
                        "vital-signs",
                        randomTime(date, 7, 22),
                        null,
                        round(randomInRange(input.range(RangeKey.SPO2, 95, 100)), 1),
                        "%",
                        "%",
                        input
                ))));
                break;
            case STEADINESS:
                repeat(input.count, () -> entries.add(entry(steadinessObservation(date, input))));
                break;
            case STEPS:
                repeat(input.count, () -> addSteps(entries, date, input));
                break;
            case TEMPERATURE:
                repeat(input.count, () -> entries.add(entry(quantityObservation(
                        "8310-5",
                        "Body temperature",
                        "HKQuantityTypeIdentifierBodyTemperature",
                        "Body Temperature",
                        "vital-signs",
                        randomTime(date, 6, 22),
                        null,
                        round(randomInRange(input.range(RangeKey.TEMPERATURE, 36, 37.3)), 1),
                        "Cel",
                        "Cel",
                        input
                ))));
                break;
            case WEIGHT:
                repeat(input.count, () -> entries.add(entry(quantityObservation(
                        "29463-7",
                        "Body weight",
                        "HKQuantityTypeIdentifierBodyMass",
                        "Body Mass",
                        "vital-signs",
                        randomTime(date, 6, 9),
                        null,
                        round(randomInRange(input.range(RangeKey.WEIGHT, 50, 120)), 1),
                        "kg",
                        "kg",
                        input
                ))));
                break;
        }
    }

    /**
     * Adds one step-count session with a realistic start and end period.
     */
    private static void addSteps(List<Object> entries, LocalDate date, HealthDataInput input) {
        Instant start = randomTime(date, 5, 22);
        Instant end = start.plusSeconds(randomInt(5, 90) * 60L);
        entries.add(entry(quantityObservation(
                "55423-8",
                "Number of steps in unspecified time Pedometer",
                "HKQuantityTypeIdentifierStepCount",
                "Step Count",
                "activity",
                start,
                end,
                randomInt(100, 2500),
                "{count}",
                "steps",
                input
        )));
    }

    /**
     * Adds systolic and diastolic blood pressure as separate supported Observations.
     */
    private static void addBloodPressure(List<Object> entries, LocalDate date, HealthDataInput input) {
        Instant time = randomTime(date, 7, 22);
        int systolic = (int) Math.round(randomInRange(input.range(RangeKey.BLOOD_PRESSURE_SYSTOLIC, 100, 170)));
        int diastolic = (int) Math.round(randomInRange(input.range(RangeKey.BLOOD_PRESSURE_DIASTOLIC, 60, 80)));

        entries.add(entry(quantityObservation(
                "8480-6",
                "Systolic blood pressure",
                "HKQuantityTypeIdentifierBloodPressureSystolic",
                "Systolic Blood Pressure",
                null,
                time,
                null,
                systolic,
                "mm[Hg]",
                "mmHg",
                input
        )));
        entries.add(entry(quantityObservation(
                "8462-4",
                "Diastolic blood pressure",
                "HKQuantityTypeIdentifierBloodPressureDiastolic",
                "Diastolic Blood Pressure",
                null,
                time,
                null,
                diastolic,
                "mm[Hg]",
                "mmHg",
                input
        )));
    }

    /**
     * Builds a standard one-value Observation with optional Apple coding and unit fields.
     */
    private static Map<String, Object> quantityObservation(
            String loincCode,
            String loincDisplay,
            String appleCode,
            String appleDisplay,
            String categoryCode,
            Instant start,
            Instant end,
            Object value,
            String unitCode,
            String unit,
            HealthDataInput input
    ) {
        Map<String, Object> observation = baseObservation(input);

        if (categoryCode != null) {
            observation.put("category", List.of(category(categoryCode)));
        }

        observation.put("code", code(loincCode, loincDisplay, appleCode, appleDisplay));

        if (end == null) {
            observation.put("effectiveDateTime", start.toString());
        } else {
            Map<String, Object> effectivePeriod = object();
            effectivePeriod.put("start", start.toString());
            effectivePeriod.put("end", end.toString());
            observation.put("effectivePeriod", effectivePeriod);
        }

        observation.put("issued", start.plusSeconds(5).toString());

        Map<String, Object> valueQuantity = object();
        valueQuantity.put("value", value);
        if (unit != null) {
            valueQuantity.put("unit", unit);
            valueQuantity.put("system", "http://unitsofmeasure.org");
        }
        if (unitCode != null) {
            valueQuantity.put("code", unitCode);
        }
        observation.put("valueQuantity", valueQuantity);

        return observation;
    }

    /**
     * Builds an ECG Observation with generated sampled voltage data.
     */
    private static Map<String, Object> ecgObservation(LocalDate date, HealthDataInput input) {
        Instant start = randomTime(date, 8, 22);
        int durationSeconds = 30;
        int sampleCount = 512 * durationSeconds;
        int heartRate = randomInt(60, 100);

        Map<String, Object> observation = baseObservation(input);
        observation.put("category", List.of(category("procedure")));
        observation.put("code", code(
                null,
                null,
                "HKElectrocardiogram",
                "Electrocardiogram"
        ));

        Map<String, Object> effectivePeriod = object();
        effectivePeriod.put("start", start.toString());
        effectivePeriod.put("end", start.plusSeconds(durationSeconds).toString());
        observation.put("effectivePeriod", effectivePeriod);
        observation.put("issued", start.plusSeconds(durationSeconds + 5).toString());

        List<Object> components = new ArrayList<>();
        Map<String, Object> sampled = object();
        sampled.put("period", 1.953125);
        sampled.put("dimensions", 1);
        sampled.put("data", generateEcgSamples(sampleCount, heartRate));
        sampled.put("origin", Map.of("value", 0));
        components.add(component("131329", "MDC_ECG_ELEC_POTL_I", sampled, null));
        components.add(component("HKElectrocardiogram.NumberOfVoltageMeasurements", "Electrocardiogram Number of Voltage Measurements", null, Map.of("unit", "measurements", "value", sampleCount)));
        components.add(component("8867-4", "Heart rate", null, Map.of("code", "/min", "system", "http://unitsofmeasure.org", "unit", "beats/minute", "value", heartRate)));
        observation.put("component", components);

        return observation;
    }

    /**
     * Builds walking steadiness with classification.
     */
    private static Map<String, Object> steadinessObservation(LocalDate date, HealthDataInput input) {
        Instant start = randomTime(date, 7, 21);
        Instant end = start.plusSeconds(randomInt(5, 30) * 60L);
        double value = round(randomDouble(0.65, 0.95), 4);

        Map<String, Object> observation = baseObservation(input);
        observation.put("code", code(null, null, "HKQuantityTypeIdentifierAppleWalkingSteadiness", "Apple Walking Steadiness"));
        observation.put("effectivePeriod", Map.of("start", start.toString(), "end", end.toString()));
        observation.put("issued", end.plusSeconds(5).toString());
        observation.put("valueQuantity", Map.of("value", value, "unit", "%", "system", "http://unitsofmeasure.org", "code", "%"));
        observation.put("component", List.of(Map.of(
                "code", code(null, null, "HKAppleWalkingSteadiness.Classification", "Walking Steadiness Classification"),
                "valueString", value >= 0.75 ? "ok" : "low"
        )));
        return observation;
    }

    /**
     * Builds sleep Observations from exact configured segments or realistic random segments.
     */
    private static List<Map<String, Object>> sleepObservations(LocalDate date, HealthDataInput input) {
        List<SleepSegment> segments = input.sleepSegments.isEmpty()
                ? randomSleepSegments(date, input.count)
                : input.sleepSegments;

        List<Map<String, Object>> observations = new ArrayList<>();
        for (SleepSegment segment : segments) {
            Instant start = sleepTime(date, segment.startTime);
            Instant end = sleepTime(date, segment.endTime);
            if (!end.isAfter(start)) {
                end = end.plus(Duration.ofDays(1));
            }

            Map<String, Object> observation = baseObservation(input);
            observation.put("category", List.of(category("activity")));
            observation.put("code", code(null, null, "HKCategoryTypeIdentifierSleepAnalysis", "Sleep Analysis"));
            observation.put("effectivePeriod", Map.of("start", start.toString(), "end", end.toString()));
            observation.put("issued", end.plusSeconds(5).toString());
            observation.put("valueString", "asleep");
            observations.add(observation);
        }
        return observations;
    }

    /**
     * Creates one to many plausible asleep periods between 8 PM and 8 AM.
     */
    private static List<SleepSegment> randomSleepSegments(LocalDate date, int maxCount) {
        List<SleepSegment> segments = new ArrayList<>();
        Instant currentStart = randomBedtime(date);
        Instant finalWake = randomWakeTime(date);
        int targetSegments = randomInt(1, Math.min(Math.max(maxCount, 1), 6));

        for (int index = 1; index <= targetSegments; index++) {
            long remainingMinutes = Duration.between(currentStart, finalWake).toMinutes();
            if (remainingMinutes < 45) {
                break;
            }

            boolean lastSegment = index == targetSegments || remainingMinutes < 120;
            Instant segmentEnd;
            if (lastSegment) {
                segmentEnd = finalWake;
            } else {
                int maxSleepMinutes = (int) Math.min(240, remainingMinutes - 35);
                segmentEnd = currentStart.plusSeconds(randomInt(45, maxSleepMinutes) * 60L);
            }

            segments.add(new SleepSegment(localSleepTime(date, currentStart), localSleepTime(date, segmentEnd)));
            currentStart = segmentEnd.plusSeconds(randomInt(5, 30) * 60L);
            if (!currentStart.isBefore(finalWake)) {
                break;
            }
        }
        return segments;
    }

    /**
     * Creates base FHIR Observation fields shared by all health types.
     */
    private static Map<String, Object> baseObservation(HealthDataInput input) {
        Map<String, Object> observation = object();
        observation.put("resourceType", "Observation");
        observation.put("status", "final");
        observation.put("extension", List.of(Map.of("url", "urn:ins:srctype", "valueString", input.sourceType)));
        observation.put("identifier", identifiers(input));
        return observation;
    }

    /**
     * Wraps one Observation in a FHIR batch entry.
     */
    private static Map<String, Object> entry(Map<String, Object> resource) {
        Map<String, Object> entry = object();
        entry.put("request", Map.of("method", "POST", "url", "Observation"));
        entry.put("resource", resource);
        return entry;
    }

    /**
     * Builds code.coding with LOINC and optional HealthKit coding.
     */
    private static Map<String, Object> code(String loincCode, String loincDisplay, String appleCode, String appleDisplay) {
        List<Object> codings = new ArrayList<>();
        if (loincCode != null) {
            codings.add(coding("http://loinc.org", loincCode, loincDisplay));
        }
        if (appleCode != null) {
            codings.add(coding("http://developer.apple.com/documentation/healthkit", appleCode, appleDisplay));
        }

        Map<String, Object> code = object();
        code.put("coding", codings);
        return code;
    }

    /**
     * Builds one coding object.
     */
    private static Map<String, Object> coding(String system, String code, String display) {
        Map<String, Object> coding = object();
        coding.put("system", system);
        coding.put("code", code);
        if (display != null) {
            coding.put("display", display);
        }
        return coding;
    }

    /**
     * Builds a FHIR Observation category.
     */
    private static Map<String, Object> category(String code) {
        String display = switch (code) {
            case "activity" -> "Activity";
            case "laboratory" -> "Laboratory";
            case "procedure" -> "Procedure";
            default -> "Vital Signs";
        };
        return Map.of("coding", List.of(Map.of(
                "system", "http://terminology.hl7.org/CodeSystem/observation-category",
                "code", code,
                "display", display
        )));
    }

    /**
     * Builds one ECG component.
     */
    private static Map<String, Object> component(String code, String display, Map<String, Object> sampledData, Map<String, Object> valueQuantity) {
        Map<String, Object> component = object();
        component.put("code", Map.of("coding", List.of(coding("http://loinc.org", code, display))));
        if (sampledData != null) {
            component.put("valueSampledData", sampledData);
        }
        if (valueQuantity != null) {
            component.put("valueQuantity", valueQuantity);
        }
        return component;
    }

    /**
     * Builds all INS identifiers for one generated Observation.
     */
    private static List<Object> identifiers(HealthDataInput input) {
        return List.of(
                Map.of("system", "urn:ins:srcid", "value", UUID.randomUUID().toString()),
                Map.of("system", "urn:ins:tenant", "value", "INS"),
                Map.of("system", "urn:ins:clientuuid", "value", input.clientUuid),
                Map.of("system", "urn:ins:fileuuid", "value", input.fileUuid),
                Map.of("system", "urn:ins:deviceuuid", "value", input.deviceUuid)
        );
    }

    /**
     * Converts a health type to the expected output file name.
     */
    private static String fileNameFor(HealthType healthType) {
        return switch (healthType) {
            case BLOOD_GLUCOSE -> "bloodGlucose.json";
            case BLOOD_PRESSURE -> "bloodPressure-data.json";
            case ECG -> "ecg.json";
            case INR -> "inr.json";
            case PULSE -> "pulse.json";
            case RESPIRATORY_RATE -> "respiratoryRate.json";
            case SLEEP -> "sleep.json";
            case SPO2 -> "spo2.json";
            case STEADINESS -> "steadiness.json";
            case STEPS -> "steps.json";
            case TEMPERATURE -> "temperature.json";
            case WEIGHT -> "weight.json";
            case ALL -> "health-data.json";
        };
    }

    /**
     * Generates ECG samples with a simple synthetic waveform.
     */
    private static String generateEcgSamples(int sampleCount, int heartRate) {
        double frequency = 512.0;
        double rr = 60.0 / heartRate;
        StringBuilder builder = new StringBuilder(sampleCount * 12);

        for (int i = 0; i < sampleCount; i++) {
            double t = i / frequency;
            double phase = (t % rr) / rr;
            double signal = 0;
            signal += gaussian(phase, 0.18, 0.030, 0.000090);
            signal += gaussian(phase, 0.365, 0.012, -0.000120);
            signal += gaussian(phase, 0.400, 0.010, 0.001000);
            signal += gaussian(phase, 0.430, 0.014, -0.000250);
            signal += gaussian(phase, 0.680, 0.070, 0.000280);
            signal += 0.000040 * Math.sin(2 * Math.PI * 0.33 * t);
            signal += randomDouble(-0.000015, 0.000015);

            if (i > 0) {
                builder.append(' ');
            }
            builder.append(String.format(Locale.US, "%.9g", signal));
        }
        return builder.toString();
    }

    /**
     * Calculates one ECG waveform peak.
     */
    private static double gaussian(double x, double center, double width, double amplitude) {
        double z = (x - center) / width;
        return amplitude * Math.exp(-0.5 * z * z);
    }

    /**
     * Picks a random instant within day hours.
     */
    private static Instant randomTime(LocalDate date, int fromHour, int toHour) {
        return date.atTime(LocalTime.of(randomInt(fromHour, toHour), randomInt(0, 59), randomInt(0, 59)))
                .toInstant(ZoneOffset.UTC);
    }

    /**
     * Picks a realistic sleep start between 8 PM and 11:30 PM.
     */
    private static Instant randomBedtime(LocalDate date) {
        int hour = randomInt(20, 23);
        int minute = hour == 23 ? randomInt(0, 30) : randomInt(0, 59);
        return date.atTime(hour, minute).toInstant(ZoneOffset.UTC);
    }

    /**
     * Picks a realistic final wake time from 5 AM to 8 AM.
     */
    private static Instant randomWakeTime(LocalDate date) {
        int hour = randomInt(5, 8);
        int minute = hour == 8 ? 0 : randomInt(0, 59);
        return date.plusDays(1).atTime(hour, minute).toInstant(ZoneOffset.UTC);
    }

    /**
     * Converts a sleep-window LocalTime to the correct overnight Instant.
     */
    private static Instant sleepTime(LocalDate sleepDate, LocalTime time) {
        LocalDate date = time.isBefore(LocalTime.NOON) || time.equals(LocalTime.NOON)
                ? sleepDate.plusDays(1)
                : sleepDate;
        return date.atTime(time).toInstant(ZoneOffset.UTC);
    }

    /**
     * Converts an Instant back into a LocalTime for sleep segment storage.
     */
    private static LocalTime localSleepTime(LocalDate sleepDate, Instant instant) {
        return instant.atOffset(ZoneOffset.UTC).toLocalDate().isAfter(sleepDate)
                ? instant.atOffset(ZoneOffset.UTC).toLocalTime()
                : instant.atOffset(ZoneOffset.UTC).toLocalTime();
    }

    /**
     * Repeats an action count times.
     */
    private static void repeat(int count, Runnable action) {
        for (int i = 0; i < count; i++) {
            action.run();
        }
    }

    /**
     * Returns a random number from a configured value range.
     */
    private static double randomInRange(ValueRange range) {
        return randomDouble(range.min, range.max);
    }

    /**
     * Returns a random integer including both ends.
     */
    private static int randomInt(int minInclusive, int maxInclusive) {
        return minInclusive + RANDOM.nextInt(maxInclusive - minInclusive + 1);
    }

    /**
     * Returns a random double between min and max.
     */
    private static double randomDouble(double minInclusive, double maxExclusive) {
        if (Double.compare(minInclusive, maxExclusive) == 0) {
            return minInclusive;
        }
        return minInclusive + (maxExclusive - minInclusive) * RANDOM.nextDouble();
    }

    /**
     * Rounds a number to the requested decimals.
     */
    private static double round(double value, int decimals) {
        double scale = Math.pow(10, decimals);
        return Math.round(value * scale) / scale;
    }

    /**
     * Builds a LinkedHashMap so JSON field order is stable.
     */
    private static Map<String, Object> object() {
        return new LinkedHashMap<>();
    }

    /**
     * Serializes simple Java Map/List/String/Number values into JSON.
     */
    private static String toJson(Object value, int indent) {
        String spaces = " ".repeat(indent);
        String childSpaces = " ".repeat(indent + 2);

        if (value instanceof Map<?, ?> map) {
            StringBuilder json = new StringBuilder("{\n");
            int index = 0;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                json.append(childSpaces)
                        .append("\"")
                        .append(escape(String.valueOf(entry.getKey())))
                        .append("\": ")
                        .append(toJson(entry.getValue(), indent + 2));
                if (index++ < map.size() - 1) {
                    json.append(",");
                }
                json.append("\n");
            }
            return json.append(spaces).append("}").toString();
        }

        if (value instanceof List<?> list) {
            StringBuilder json = new StringBuilder("[\n");
            for (int i = 0; i < list.size(); i++) {
                json.append(childSpaces).append(toJson(list.get(i), indent + 2));
                if (i < list.size() - 1) {
                    json.append(",");
                }
                json.append("\n");
            }
            return json.append(spaces).append("]").toString();
        }

        if (value instanceof String text) {
            return "\"" + escape(text) + "\"";
        }

        if (value instanceof Number || value instanceof Boolean) {
            return String.valueOf(value);
        }

        if (value == null) {
            return "null";
        }

        return "\"" + escape(String.valueOf(value)) + "\"";
    }

    /**
     * Escapes JSON string characters.
     */
    private static String escape(String value) {
        return value.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    public enum HealthType {
        ALL,
        BLOOD_GLUCOSE,
        BLOOD_PRESSURE,
        ECG,
        INR,
        PULSE,
        RESPIRATORY_RATE,
        SLEEP,
        SPO2,
        STEADINESS,
        STEPS,
        TEMPERATURE,
        WEIGHT
    }

    public enum RangeKey {
        SPO2,
        RESPIRATORY_RATE,
        PULSE,
        BLOOD_PRESSURE_SYSTOLIC,
        BLOOD_PRESSURE_DIASTOLIC,
        INR,
        TEMPERATURE,
        BLOOD_GLUCOSE,
        WEIGHT
    }

    public static class HealthDataInput {
        public final HealthType healthType;
        public final LocalDate startDate;
        public final LocalDate endDate;
        public final String clientUuid;
        public final String fileUuid;
        public final String deviceUuid;
        public final String sourceType;
        public final int count;
        public final List<SleepSegment> sleepSegments;
        public final Map<RangeKey, ValueRange> customRanges;

        /**
         * Stores all class-based input needed to generate health data.
         */
        public HealthDataInput(
                HealthType healthType,
                LocalDate startDate,
                LocalDate endDate,
                String clientUuid,
                String fileUuid,
                String deviceUuid,
                String sourceType,
                int count,
                List<SleepSegment> sleepSegments,
                Map<RangeKey, ValueRange> customRanges
        ) {
            if (startDate.isAfter(endDate)) {
                throw new IllegalArgumentException("startDate must be before or equal to endDate");
            }
            if (count <= 0) {
                throw new IllegalArgumentException("count must be greater than 0");
            }

            this.healthType = healthType;
            this.startDate = startDate;
            this.endDate = endDate;
            this.clientUuid = clientUuid;
            this.fileUuid = fileUuid;
            this.deviceUuid = deviceUuid;
            this.sourceType = sourceType;
            this.count = count;
            this.sleepSegments = sleepSegments == null ? List.of() : new ArrayList<>(sleepSegments);
            this.customRanges = customRanges == null ? Map.of() : new LinkedHashMap<>(customRanges);
        }

        /**
         * Copies input and changes only health type.
         */
        public HealthDataInput withHealthType(HealthType nextType) {
            return new HealthDataInput(nextType, startDate, endDate, clientUuid, fileUuid, deviceUuid, sourceType, count, sleepSegments, customRanges);
        }

        /**
         * Gets custom range or fallback range.
         */
        public ValueRange range(RangeKey key, double defaultMin, double defaultMax) {
            return customRanges.getOrDefault(key, new ValueRange(defaultMin, defaultMax));
        }
    }

    public static class SleepSegment {
        public final LocalTime startTime;
        public final LocalTime endTime;

        /**
         * Stores one sleep period in the 8 PM to 8 AM sleep window.
         */
        public SleepSegment(LocalTime startTime, LocalTime endTime) {
            this.startTime = startTime;
            this.endTime = endTime;
        }
    }

    public static class ValueRange {
        public final double min;
        public final double max;

        /**
         * Stores min and max values for generated measurements.
         */
        public ValueRange(double min, double max) {
            if (min > max) {
                throw new IllegalArgumentException("min must be less than or equal to max");
            }
            this.min = min;
            this.max = max;
        }
    }

    public static class HealthDataInputConfig {
        /**
         * Edit this method to control all generator input from class code.
         */
        public static HealthDataInput input() {
            return new HealthDataInput(
                    HealthType.ALL,
                    LocalDate.parse("2026-06-09"),
                    LocalDate.parse("2026-06-10"),
                    "8f8490fc-d51b-4eb6-9d70-67944488f081",
                    "3673fea5-3a6c-44c6-80cc-52cf1bcc7c8a",
                    "9abfc0a1-6c3e-4fe6-899f-850c26171fe7",
                    "Apple Watch",
                    10,
                    List.of(),
                    Map.of(
                            RangeKey.INR, new ValueRange(1.9, 3.1),
                            RangeKey.PULSE, new ValueRange(50, 120),
                            RangeKey.BLOOD_PRESSURE_SYSTOLIC, new ValueRange(100, 170),
                            RangeKey.BLOOD_PRESSURE_DIASTOLIC, new ValueRange(60, 80)
                    )
            );
        }
    }
}

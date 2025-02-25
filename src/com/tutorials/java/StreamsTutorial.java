package com.tutorials.java;

import java.util.Arrays;
import java.util.List;

public class StreamsTutorial {

    private final List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9);
    private static final List<String> strings = Arrays.asList("apple", "banana", "grapes", "dragon fruit", "kiwi");

    public int calculateSum() {
        return numbers.stream().mapToInt(Integer::intValue).sum();
    }

    public int calculateEvenNumberSum() {
        return numbers.stream().filter(number -> number % 2 == 0).mapToInt(Integer::intValue).sum();
    }

    public long countStrLengthGreaterThanFour() {
        return strings.stream().filter(s -> s.length() > 4).count();
    }

    public static void main(String[] args) {
        StreamsTutorial streamsTutorial = new StreamsTutorial();
        // sum of all integers
        System.out.println(streamsTutorial.calculateSum());
        System.out.println(streamsTutorial.calculateEvenNumberSum());
        System.out.println(streamsTutorial.countStrLengthGreaterThanFour());
    }
}

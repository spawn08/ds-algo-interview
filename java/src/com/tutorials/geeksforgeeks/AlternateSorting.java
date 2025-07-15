package com.tutorials.geeksforgeeks;

import java.util.Arrays;

/**
 * Given an array of integers, print the array in such a way
 * that the first element is first maximum and second element is first minimum and so on.
 * <p>
 * Examples :
 * <p>
 * Input : arr[] = {7, 1, 2, 3, 4, 5, 6}
 * Output : 7 1 6 2 5 3 4
 * <p>
 * Input : arr[] = {1, 6, 9, 4, 3, 7, 8, 2}
 * Output : 9 1 8 2 7 3 6 4
 *
 * @link <a href="https://www.geeksforgeeks.org/alternative-sorting/">...</a>
 */
public class AlternateSorting {

    /**
     * Method sorts and prints the array elements in alternate sorting order
     *
     * @param input array input
     * @return
     */
    public int[] alternateSorting(int[] input) {
        int[] alternateSort = new int[input.length];
        int alternateIndex = 0;
        int size = input.length;
        int firstIndex = 0;
        int lastIndex = size - 1;
        Arrays.sort(input);

        while (firstIndex < lastIndex) {
            alternateSort[alternateIndex] = input[lastIndex--];
            alternateIndex += 1;
            alternateSort[alternateIndex] = input[firstIndex++];
            alternateIndex += 1;
            System.out.print(input[lastIndex--] + " ");
            System.out.print(input[firstIndex++] + " ");
        }

        if (size % 2 != 0) {
            alternateSort[alternateIndex] = input[firstIndex];
            System.out.print(input[firstIndex] + " ");
        }

        return alternateSort;
    }

    public static void main(String[] args) {
        int[] input = {7, 1, 2, 3, 4, 5, 6};
        AlternateSorting alternateSorting = new AlternateSorting();
        alternateSorting.alternateSorting(input);
        System.out.println(Arrays.toString(alternateSorting.alternateSorting(input)));
    }
}
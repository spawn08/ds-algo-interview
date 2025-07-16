package com.tutorials.algorithms;

import java.util.Arrays;

public class BinarySearch {

    public static boolean binarySearchIterative(int[] inputArray, int target) {
        int lowerIndex = 0;
        int higherIndex = inputArray.length - 1;

        while(lowerIndex <= higherIndex) {
            int middleIndex = lowerIndex + (higherIndex - lowerIndex) / 2;
            if(inputArray[middleIndex] == target) return true;

            if(inputArray[middleIndex] > target) {
                higherIndex = middleIndex - 1;
            } else lowerIndex = middleIndex + 1;
        }

        return false;
    }

    public static boolean binarySearchRecursive(int[] inputArray, int lowerIndex, int higherIndex, int target) {
        while(lowerIndex <= higherIndex) {
            int middleIndex = lowerIndex + (higherIndex - lowerIndex) / 2;
            if(inputArray[middleIndex] == target) return true;
            if(inputArray[middleIndex] > target) return binarySearchRecursive(inputArray, lowerIndex, middleIndex - 1,  target);
            else return binarySearchRecursive(inputArray, middleIndex - 1, higherIndex, target);
        }
        return false;
    }

    public static void main(String[] args) {
        int[] arr = {2,3,4,5,1,7,9,10};
        Arrays.sort(arr);
        System.out.println(BinarySearch.binarySearchIterative(arr, 0));
        System.out.println(BinarySearch.binarySearchRecursive(arr, 0, arr.length - 1, 0));
    }
}

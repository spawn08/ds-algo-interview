package com.tutorials.problems;

/**
 * There are n buckets arranged in a row. Each bucket either is empty or contains a ball. The buckets are specified
 * as a string buckets consisting of characters '.' and 'B' in one move you can take the ball out of any bucket
 * and place it in another empty bucket. your goal is to arrange the balls to create an alternating sequence of full and empty buckets.
 * distance between two consecutive balls should be equal to 2, note that the sequence may start at any bucket
 * we need to give what is minimum numbers of moves required to create a correct sequence of balls in bucket.
 * If it is impossible return -1
 * <p>
 * Sample Input 1:
 * BB.B.BBB...
 * Sample Output 1:
 * 4
 * <p>
 * Sample Input 2:
 * ..B....B.BB
 * Sample Output 2:
 * 2
 */
public class BucketsProblem {

    /**
     * Calculate minimum moves required to arrange balls in alternating seqyence
     *
     * @param buckets string input
     * @return minMoves integer value
     */
    public static int minMoves(String buckets) {
        int bucketsLength = buckets.length();
        int ballCount = 0;
        int minimumMoves;

        for (int index = 0; index < bucketsLength; index++) {
            if (buckets.charAt(index) == 'B') {
                ballCount++;
            }
        }

        if (ballCount > (bucketsLength + 1) / 2) return -1;
        minimumMoves = ballCount;

        int correctBallPosition = 0;
        for (int index = 0; index < bucketsLength; index = index + 2) {
            if (buckets.charAt(index) == 'B') {
                correctBallPosition++;
            }
        }

        minimumMoves = Math.min(minimumMoves, ballCount - correctBallPosition);
        return minimumMoves;
    }

    public static void main(String[] args) {
        String buckets = "BB.B.BBB..."; //..B....B.BB; BB.B.BBB...; BB.B..
        System.out.println(BucketsProblem.minMoves(buckets));
    }
}

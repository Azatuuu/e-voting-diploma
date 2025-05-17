pragma circom 2.0.0;

template VoteCheck() {
    signal input vote;
    signal output is_valid;

    // Проверка, что голос — 0 или 1 (результат должен быть 0)
    is_valid <== vote * (1 - vote);
}

component main = VoteCheck();

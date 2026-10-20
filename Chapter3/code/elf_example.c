int initialized = 42;
int uninitialized;

int main(void) {
    uninitialized = initialized + 1;
    return uninitialized;
}

export async function pollUntil<T>(
  operation: () => Promise<T>,
  isComplete: (value: T) => boolean,
  options: { timeoutMs: number; intervalMs: number; description: string },
): Promise<T> {
  const deadline = Date.now() + options.timeoutMs;
  let lastValue: T;
  while (true) {
    lastValue = await operation();
    if (isComplete(lastValue)) return lastValue;
    if (Date.now() >= deadline) {
      throw new Error(`Timed out waiting for ${options.description}.`);
    }
    await new Promise(resolve => setTimeout(resolve, options.intervalMs));
  }
}

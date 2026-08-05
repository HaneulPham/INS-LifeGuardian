export type CleanupAction = () => Promise<void>;

type RegisteredCleanup = { label: string; action: CleanupAction };

export class CleanupRegistry {
  private readonly actions: RegisteredCleanup[] = [];

  register(label: string, action: CleanupAction): void {
    this.actions.push({ label, action });
  }

  async run(): Promise<void> {
    const failures: string[] = [];
    for (const item of this.actions.reverse()) {
      try {
        await item.action();
      } catch (error) {
        failures.push(`${item.label}: ${error instanceof Error ? error.message : String(error)}`);
      }
    }
    if (failures.length) {
      throw new Error(`Cleanup failed:\n${failures.join('\n')}`);
    }
  }
}

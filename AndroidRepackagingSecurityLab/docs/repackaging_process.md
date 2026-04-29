## 🔬 Repackaging Workflow (High-Level)

The experiment followed a structured APK modification workflow:

1. **APK Analysis**

   * A legitimate application was selected and decompiled
   * Internal structure and entry points were analyzed

2. **Code Injection Simulation**

   * Additional logic was introduced into the application flow
   * Execution was triggered from the main activity lifecycle

3. **Permission Adjustment**

   * The application manifest was modified to enable network capabilities

4. **Rebuild & Alignment**

   * The application was rebuilt and aligned for runtime compatibility

5. **Application Signing**

   * A custom key was generated and used to sign the modified APK

---

## 🧠 Key Insight

This process demonstrates how attackers can alter legitimate applications and why:

* APK integrity validation is critical
* App stores enforce strict signing policies
* Users should avoid third-party APK sources

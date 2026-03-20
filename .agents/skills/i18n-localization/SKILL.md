---
name: i18n-localization
description: "Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support."
---

# i18n & Localization

> Internationalization (i18n) and Localization (L10n) best practices.

---

## 1. Core Concepts

| Term | Meaning |
|------|---------|
| **i18n** | Internationalization - making app translatable |
| **L10n** | Localization - actual translations |
| **Locale** | Language + Region (en-US, tr-TR) |
| **RTL** | Right-to-left languages (Arabic, Hebrew) |

---

## 2. When to Use i18n

| Project Type | i18n Needed? |
|--------------|--------------|
| Public web app | ✅ Yes |
| SaaS product | ✅ Yes |
| Internal tool | ⚠️ Maybe |
| Single-region app | ⚠️ Consider future |
| Personal project | ❌ Optional |

---

## 3. Implementation Patterns

### Vue (i18next-vue)

```vue
<script setup lang="ts">
import { computed } from 'vue'
import { useTranslation } from 'i18next-vue'

const { t } = useTranslation()

const title = computed(() => t('welcome.title'))

function getRequiredRule() {
  return { required: true, message: t('form.required') }
}
</script>

<template>
  <h1>{{ $t('welcome.title') }}</h1>
  <p>{{ title }}</p>
  <p>{{ getRequiredRule().message }}</p>
</template>
```

### Python (gettext)

```python
from gettext import gettext as _

print(_("Welcome to our app"))
```

---

## 4. File Structure

Frontend locales:

```
locales/
├── en-US.json
├── zh-CN.json
├── ar-SA.json        # RTL
```
---

## 5. Terminology

See [terminology.md](references/terminology.md).

- Keep UI naming consistent (应用/Application, 控制台/Console)
- Do not translate product names and code identifiers

---

## 6. Best Practices

See [best-practices.md](references/best-practices.md).

- Use translation keys and namespaces
- Avoid string concatenation; use placeholders/plurals
- Format dates/numbers by locale; allow text expansion/RTL

---

## 7. Checklist

- [ ] No hardcoded user-facing strings
- [ ] Locale files exist for all supported languages
- [ ] Fallback language is configured
- [ ] i18n checker script passes
- [ ] Terminology follows the project glossary

---

## Script

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/i18n_checker.py` | Detect hardcoded strings & missing translations | `python scripts/i18n_checker.py <project_path>` |

## When to Use
Use this skill to audit i18n usage and locale completeness.

# Theme Fields Reference

All fields of `Term.Theme`. Create with keyword args: `Theme(field=value, ...)`.

## General

| Field | Default | Description |
|-------|---------|-------------|
| `name` | `"default"` | Theme name |

## Syntax Highlighting

| Field | Default | Used by |
|-------|---------|---------|
| `docstring` | green_dark | highlight |
| `string` | `"#64b565"` | highlight |
| `type` | purple_light | highlight |
| `code` | yellow | highlight |
| `multiline_code` | yellow | highlight |
| `symbol` | orange | highlight |
| `expression` | amber | highlight |
| `number` | blue_light | highlight |
| `operator` | red | highlight |
| `func` | `"#f2d777"` | highlight |
| `link` | `"underline $(light_blue_light)"` | highlight |

## Text

| Field | Default | Used by |
|-------|---------|---------|
| `text` | `"default"` | General text |
| `text_accent` | `"white"` | Accented text |
| `emphasis` | `"$blue bold"` | Emphasis |
| `emphasis_light` | yellow_light | Light emphasis |

## Lines and Boxes

| Field | Default | Used by |
|-------|---------|---------|
| `line` | `"default"` | Panel, hLine, vLine border style |
| `box` | `:ROUNDED` | Panel, hLine, vLine box type |

## Logging

| Field | Default | Used by |
|-------|---------|---------|
| `info` | `"#7cb0cf"` | @info log level |
| `debug` | `"#197fbd"` | @debug log level |
| `warn` | orange | @warn log level |
| `error` | `"bold #d13f3f"` | @error log level |
| `logmsg` | `"#8abeff"` | Log message text |

## Tree

| Field | Default | Used by |
|-------|---------|---------|
| `tree_mid` | blue | Mid-branch guide |
| `tree_terminator` | blue | Terminal branch guide |
| `tree_skip` | blue | Skip guide |
| `tree_dash` | blue | Dash guide |
| `tree_trunc` | blue | Truncation indicator |
| `tree_pair` | red_light | Key-value pair |
| `tree_keys` | yellow | Key names |
| `tree_title` | `"bold " * orange` | Tree title |
| `tree_max_leaf_width` | `44` | Max width per leaf (Int) |

## Repr

| Field | Default | Used by |
|-------|---------|---------|
| `repr_accent` | `"bold #e0db79"` | termshow accent |
| `repr_name` | `"#e3ac8d"` | Type name |
| `repr_type` | `"#bb86db"` | Field types |
| `repr_values` | `"#b3d4ff"` | Field values |
| `repr_line` | `"dim #7e9dd9"` | Separator lines |
| `repr_panel` | `"#9bb3e0"` | Panel border |
| `repr_array_panel` | `"dim yellow"` | Array panel |
| `repr_array_title` | `"dim bright_blue"` | Array title |
| `repr_array_text` | `"bright_blue"` | Array text |

## Errors

| Field | Default | Used by |
|-------|---------|---------|
| `err_accent` | pink | Error accent |
| `er_bt` | `"#ff8a4f"` | Backtrace |
| `err_btframe_panel` | `"#9bb3e0"` | Frame panel |
| `err_filepath` | `"grey62"` | File paths |
| `err_errmsg` | `"red"` | Error message |

## Introspection

| Field | Default | Used by |
|-------|---------|---------|
| `inspect_highlight` | pink_light | Highlight |
| `inspect_accent` | pink | Accent |

## Progress

| Field | Default | Used by |
|-------|---------|---------|
| `progress_accent` | pink | Progress bar accent |
| `progress_elapsedcol_default` | purple_light | Elapsed column |
| `progress_etacol_default` | teal | ETA column |
| `progress_spiner_default` | `"bold blue"` | Spinner |
| `progress_spinnerdone_default` | `"green bold"` | Completed spinner |

## Dendogram

| Field | Default | Used by |
|-------|---------|---------|
| `dendo_title` | salmon_light | Dendogram title |
| `dendo_pretitle` | blue_grey_light | Pre-title |
| `dendo_leaves` | blue_grey_light | Leaves |
| `dendo_lines` | `"$blue_light dim bold"` | Connecting lines |

## Markdown

| Field | Default | Used by |
|-------|---------|---------|
| `md_h1` | `"bold $indigo_light"` | H1 headers |
| `md_h2` | `"bold $blue underline"` | H2 headers |
| `md_h3` | `"bold $blue"` | H3 headers |
| `md_h4` | `"bold $light_blue"` | H4 headers |
| `md_h5` | `"bold $cyan_light"` | H5 headers |
| `md_h6` | `"bold $cyan_lighter"` | H6 headers |
| `md_latex` | `"$yellow_light italic"` | LaTeX |
| `md_code` | `"$yellow_light italic"` | Inline code |
| `md_codeblock_bg` | `"#202020"` | Code block background |
| `md_quote` | `"#5a74f2"` | Blockquotes |
| `md_footnote` | `"#9aacdb"` | Footnotes |
| `md_table_header` | `"bold yellow"` | Table headers |
| `md_admonition_note` | `"blue"` | Note admonition |
| `md_admonition_info` | `"blue"` | Info admonition |
| `md_admonition_warning` | yellow_light | Warning admonition |
| `md_admonition_danger` | `"red"` | Danger admonition |
| `md_admonition_tip` | `"green"` | Tip admonition |

## Table

| Field | Default | Used by |
|-------|---------|---------|
| `tb_style` | `"#9bb3e0"` | Table border |
| `tb_header` | `"bold white"` | Header text |
| `tb_columns` | `"default"` | Column text |
| `tb_footer` | `"default"` | Footer text |
| `tb_box` | `:MINIMAL_HEAVY_HEAD` | Table box type |

## Prompt

| Field | Default | Used by |
|-------|---------|---------|
| `prompt_text` | blue | Prompt text |
| `prompt_default_option` | `"underline bold $green"` | Default option |
| `prompt_options` | `"default"` | Options |

## Annotations

| Field | Default | Used by |
|-------|---------|---------|
| `annotation_color` | blue_light | Annotation color |

## Pre-built Themes

- `Theme()` / `DarkTheme` -- default, optimized for dark terminals
- `LightTheme` -- adjusted for light backgrounds

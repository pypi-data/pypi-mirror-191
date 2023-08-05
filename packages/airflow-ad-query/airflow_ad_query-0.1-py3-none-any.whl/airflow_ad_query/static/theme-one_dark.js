// Copyright 2022 wano
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

ace.define("ace/theme/one_dark", ["require", "exports", "module", "ace/lib/dom"], function (e, t, n) {
    t.isDark = !0, t.cssClass = "ace-one-dark", t.cssText = ".ace-one-dark .ace_gutter {background: #282c34;color: #6a6f7a}.ace-one-dark .ace_print-margin {width: 1px;background: #e8e8e8}.ace-one-dark {background-color: #282c34;color: #abb2bf}.ace-one-dark .ace_cursor {color: #528bff}.ace-one-dark .ace_marker-layer .ace_selection {background: #3d4350}.ace-one-dark.ace_multiselect .ace_selection.ace_start {box-shadow: 0 0 3px 0 #282c34;border-radius: 2px}.ace-one-dark .ace_marker-layer .ace_step {background: #c6dbae}.ace-one-dark .ace_marker-layer .ace_bracket {margin: -1px 0 0 -1px;border: 1px solid #747369}.ace-one-dark .ace_marker-layer .ace_active-line {background: rgba(76, 87, 103, .19)}.ace-one-dark .ace_gutter-active-line {background-color: rgba(76, 87, 103, .19)}.ace-one-dark .ace_marker-layer .ace_selected-word {border: 1px solid #3d4350}.ace-one-dark .ace_fold {background-color: #61afef;border-color: #abb2bf}.ace-one-dark .ace_keyword {color: #c678dd}.ace-one-dark .ace_keyword.ace_operator {color: #c678dd}.ace-one-dark .ace_keyword.ace_other.ace_unit {color: #d19a66}.ace-one-dark .ace_constant.ace_language {color: #d19a66}.ace-one-dark .ace_constant.ace_numeric {color: #d19a66}.ace-one-dark .ace_constant.ace_character {color: #56b6c2}.ace-one-dark .ace_constant.ace_other {color: #56b6c2}.ace-one-dark .ace_support.ace_function {color: #61afef}.ace-one-dark .ace_support.ace_constant {color: #d19a66}.ace-one-dark .ace_support.ace_class {color: #e5c07b}.ace-one-dark .ace_support.ace_type {color: #e5c07b}.ace-one-dark .ace_storage {color: #c678dd}.ace-one-dark .ace_storage.ace_type {color: #c678dd}.ace-one-dark .ace_invalid {color: #fff;background-color: #f2777a}.ace-one-dark .ace_invalid.ace_deprecated {color: #272b33;background-color: #d27b53}.ace-one-dark .ace_string {color: #98c379}.ace-one-dark .ace_string.ace_regexp {color: #e06c75}.ace-one-dark .ace_comment {font-style: italic;color: #5c6370}.ace-one-dark .ace_variable {color: #e06c75}.ace-one-dark .ace_variable.ace_parameter {color: #d19a66}.ace-one-dark .ace_meta.ace_tag {color: #e06c75}.ace-one-dark .ace_entity.ace_other.ace_attribute-name {color: #e06c75}.ace-one-dark .ace_entity.ace_name.ace_function {color: #61afef}.ace-one-dark .ace_entity.ace_name.ace_tag {color: #e06c75}.ace-one-dark .ace_markup.ace_heading {color: #98c379}.ace-one-dark .ace_indent-guide {background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAEklEQVQImWPQ09NrYAgMjP4PAAtGAwchHMyAAAAAAElFTkSuQmCC) right repeat-y}";
    var r = e("../lib/dom");
    r.importCssString(t.cssText, t.cssClass, !1)
});
(function () {
    ace.require(["ace/theme/one_dark"], function (m) {
        if (typeof module == "object" && typeof exports == "object" && module) {
            module.exports = m;
        }
    });
})();
            

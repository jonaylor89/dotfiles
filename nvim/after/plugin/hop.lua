local hop = require'hop'

vim.keymap.set("n", "<leader>hw", "<cmd>HopWord<CR>")
vim.keymap.set("n", "<leader>hl", "<cmd>HopLine<CR>")
vim.keymap.set("n", "<leader>hp", "<cmd>HopPattern<CR>")

hop.setup()

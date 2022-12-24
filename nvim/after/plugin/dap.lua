local dap = require'dap'
local dap_go = require'dap-go'
local dap_ui = require'dapui'

dap.adapters.lldb = {
  type = 'executable',
  command = '/usr/bin/lldb', -- adjust as needed, must be absolute path
  name = 'lldb'
}
dap.configurations.rust = dap.configurations.lldb

vim.keymap.set("n", "<F1>", function() dap.step_into() end)
vim.keymap.set("n", "<F2>", function() dap.step_over() end)
vim.keymap.set("n", "<F3>", function() dap.step_out() end)
vim.keymap.set("n", "<F4>", function() dap.continue() end)
vim.keymap.set("n", "<leader>b", function() dap.toggle_breakpoint() end)
vim.keymap.set("n", "<leader>B", function() dap.set_breakpoint(vim.fn.input('Breakpoint condition: ')) end)
vim.keymap.set("n", "<leader>lp", function() dap.set_breakpoint(nil, nil, vim.fn.input('Log point message: ')) end)
vim.keymap.set("n", "<leader>dr", function() dap.repl.open() end)


vim.keymap.set("n", "<leader>dt", function() dap_go.debug_test() end)


require("nvim-dap-virtual-text").setup()
dap_go.setup()
dap_ui.setup()

dap.listeners.after.event_initialized["dapui_config"] = function() 
    dap_ui.open()
end
dap.listeners.before.event_terminated["dapui_config"] = function() 
    dap_ui.close()
end
dap.listeners.before.event_exited["dapui_config"] = function() 
    dap_ui.close()
end

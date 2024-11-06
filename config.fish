alias ls='exa -A'
alias cat='bat -p'
alias hx='helix'

alias gc='git clone'
alias cb='git checkout'
alias nb='git checkout -b'

zoxide init --cmd cd fish | source

export PATH="/home/me/.local/bin:/home/me/.cargo/bin:$PATH"

function fish_greeting
end

function fish_prompt
    set -l last_status $status
    if test $last_status -ne 0
        set_color red
        echo "Exited with error code: $last_status"
    end

    # Git branch and status
    set -l git_branch (fish_git_prompt | string trim)
    if test -n "$git_branch"
        set git_branch " $git_branch"
    end

    string join '' -- (set_color green) (prompt_pwd --full-length-dirs 2) (set_color magenta) "$git_branch" (set_color normal) ' > '
end

FROM archlinux:base-devel

# Initialize User
RUN pacman -Sy --noconfirm bash
RUN useradd -ms /bin/bash me

# Install terminal
RUN pacman -Sy --noconfirm alacritty xorg ttf-firacode-nerd

# Configure Sudo
RUN echo "me ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Install Shell
RUN pacman -Sy --noconfirm fish zellij zoxide fzf bat exa

# Configure Editor
RUN pacman -Sy --noconfirm helix

# Install All LSP
RUN pacman -Sy --noconfirm python-pygls python-pip python-pipx \
                           clang python-lsp-server bash-language-server \
                           vscode-css-languageserver vscode-html-languageserver \
                           vscode-json-languageserver yaml-language-server
RUN su me -c 'pip install --break-system-packages c_formatter_42'
RUN su me -c 'pipx install norminette'
COPY --chown=me:me norminette_lsp.py /home/me/.local/bin/norminette_lsp.py
RUN chmod +x /home/me/.local/bin/norminette_lsp.py
COPY --chown=me:me norminette_fmt.py /home/me/.local/bin/norminette_fmt.py
RUN chmod +x /home/me/.local/bin/norminette_fmt.py

# Adding utilities
RUN pacman -Sy --noconfirm git git-lfs less openssh docker valgrind xclip

# Adding configurations
COPY --chown=me:me alacritty.toml /home/me/.config/alacritty/alacritty.toml
COPY --chown=me:me config.fish /home/me/.config/fish/config.fish
COPY --chown=me:me helix.toml /home/me/.config/helix/config.toml
COPY --chown=me:me helix_theme.toml /home/me/.config/helix/themes/catppuccin_mocha.toml
COPY --chown=me:me languages.toml /home/me/.config/helix/languages.toml
COPY --chown=me:me config.kdl /home/me/.config/zellij/config.kdl
COPY --chown=me:me gitconfig /home/me/.gitconfig

# Configure volumes
VOLUME /home/me/.ssh
VOLUME /home/me/.cache
VOLUME /home/me/.local/share/fish
VOLUME /home/me/.local/share/zoxide
VOLUME /home/me/projects

# Server start
WORKDIR /home/me
COPY start.sh /
RUN chmod +x /start.sh
USER me
ENTRYPOINT ["/start.sh"]


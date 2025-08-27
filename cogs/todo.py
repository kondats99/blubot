import discord
from discord.ext import commands

class Todo(commands.Cog):
    """Cog for todo list functionality."""
    
    def __init__(self, bot):
        self.bot = bot
        # Store todos per user (user_id -> list of todos)
        self.todos = {}

    def get_user_todos(self, user_id):
        """Get todos for a specific user."""
        if user_id not in self.todos:
            self.todos[user_id] = []
        return self.todos[user_id]

    @commands.group(name="todo", invoke_without_command=True)
    async def todo(self, ctx):
        """Manage your personal todo list."""
        if ctx.invoked_subcommand is None:
            # Show custom help when just %todo is used
            embed = discord.Embed(
                title="📝 Todo List Commands",
                description="Manage your personal todo list with these commands:",
                color=discord.Color.blue()
            )
            
            commands_list = (
                "✏️ `%todo add <task>` — Add a new task\n"
                "📋 `%todo list` — List all your tasks\n"
                "✅ `%todo done <task_id>` — Mark a task as done\n"
                "🗑️ `%todo remove <task_id>` — Remove a task\n"
                "🧹 `%todo clear` — Clear all tasks"
            )
            
            embed.add_field(name="Available Commands", value=commands_list, inline=False)
            embed.add_field(name="Examples", value="`%todo add Buy groceries`\n`%todo done 1`", inline=False)
            embed.set_footer(text="Use %help todo <command> for detailed help on a specific command")
            
            await ctx.send(embed=embed)

    @todo.command(name="add")
    async def add_todo(self, ctx, *, task: str):
        """Add a new task to your todo list."""
        user_todos = self.get_user_todos(ctx.author.id)
        user_todos.append(task)
        
        embed = discord.Embed(
            title="✅ Task Added",
            description=f"Added: **{task}**",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"You now have {len(user_todos)} task(s)")
        await ctx.send(embed=embed)

    @todo.command(name="list")
    async def list_todos(self, ctx):
        """List all your current tasks."""
        user_todos = self.get_user_todos(ctx.author.id)
        
        if not user_todos:
            embed = discord.Embed(
                title="📝 Your Todo List",
                description="No tasks found! Use `%todo add <task>` to add one.",
                color=discord.Color.blue()
            )
        else:
            task_list = "\n".join([f"**{i+1}.** {task}" for i, task in enumerate(user_todos)])
            embed = discord.Embed(
                title="📝 Your Todo List",
                description=task_list,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Total: {len(user_todos)} task(s)")
        
        await ctx.send(embed=embed)

    @todo.command(name="done")
    async def complete_todo(self, ctx, task_id: int):
        """Mark a task as done and remove it from your list."""
        user_todos = self.get_user_todos(ctx.author.id)
        
        if not user_todos:
            await ctx.send("❌ Your todo list is empty!")
            return
        
        if task_id < 1 or task_id > len(user_todos):
            await ctx.send(f"❌ Invalid task ID! Use a number between 1 and {len(user_todos)}.")
            return
        
        completed_task = user_todos.pop(task_id - 1)
        
        embed = discord.Embed(
            title="🎉 Task Completed",
            description=f"Completed: **{completed_task}**",
            color=discord.Color.yellow()
        )
        embed.set_footer(text=f"You have {len(user_todos)} task(s) remaining")
        await ctx.send(embed=embed)

    @todo.command(name="remove")
    async def remove_todo(self, ctx, task_id: int):
        """Remove a task from your todo list without marking it as done."""
        user_todos = self.get_user_todos(ctx.author.id)
        
        if not user_todos:
            await ctx.send("❌ Your todo list is empty!")
            return
        
        if task_id < 1 or task_id > len(user_todos):
            await ctx.send(f"❌ Invalid task ID! Use a number between 1 and {len(user_todos)}.")
            return
        
        removed_task = user_todos.pop(task_id - 1)
        
        embed = discord.Embed(
            title="🗑️ Task Removed",
            description=f"Removed: **{removed_task}**",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"You have {len(user_todos)} task(s) remaining")
        await ctx.send(embed=embed)

    @todo.command(name="clear")
    async def clear_todos(self, ctx):
        """Clear all tasks from your todo list."""
        user_todos = self.get_user_todos(ctx.author.id)
        
        if not user_todos:
            await ctx.send("❌ Your todo list is already empty!")
            return
        
        task_count = len(user_todos)
        user_todos.clear()
        
        embed = discord.Embed(
            title="🧹 Todo List Cleared",
            description=f"Removed all {task_count} task(s) from your todo list.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    cog = Todo(bot)
    await bot.add_cog(cog)
    
    # Set custom help attributes for the todo group
    main_cmd = cog.todo
    main_cmd.callback.help_title = "📝 Todo List Commands"
    main_cmd.callback.help_description = "Manage your personal todo list with these commands:"
    main_cmd.callback.help_commands = (
        "✏️ `%todo add <task>` — Add a new task\n"
        "📋 `%todo list` — List all your tasks\n"
        "✅ `%todo done <task_id>` — Mark a task as done\n"
        "🗑️ `%todo remove <task_id>` — Remove a task\n"
        "🧹 `%todo clear` — Clear all tasks"
    )
    main_cmd.callback.help_examples = "`%todo add Buy groceries`\n`%todo done 1`"
    
    # Set help attributes for individual subcommands
    add_cmd = cog.add_todo
    add_cmd.callback.help_description = "Add a new task to your todo list."
    add_cmd.callback.help_usage = "%todo add <task>"
    add_cmd.callback.help_example = "%todo add Buy groceries"
    
    list_cmd = cog.list_todos
    list_cmd.callback.help_description = "List all your current tasks."
    list_cmd.callback.help_usage = "%todo list"
    list_cmd.callback.help_example = "%todo list"
    
    done_cmd = cog.complete_todo
    done_cmd.callback.help_description = "Mark a task as done and remove it from your list."
    done_cmd.callback.help_usage = "%todo done <task_id>"
    done_cmd.callback.help_example = "%todo done 1"
    
    remove_cmd = cog.remove_todo
    remove_cmd.callback.help_description = "Remove a task from your todo list without marking it as done."
    remove_cmd.callback.help_usage = "%todo remove <task_id>"
    remove_cmd.callback.help_example = "%todo remove 2"
    
    clear_cmd = cog.clear_todos
    clear_cmd.callback.help_description = "Clear all tasks from your todo list."
    clear_cmd.callback.help_usage = "%todo clear"
    clear_cmd.callback.help_example = "%todo clear"
<script lang="ts">
  type ButtonSize = 'sm' | 'md' | 'lg';
  type ButtonType = 'iconOnly' | 'withText';
  export let text: string = '';
  export let extra: string = '';
  export let size: ButtonSize = 'md';
  let buttonType: ButtonType = (!text && !extra) ? 'iconOnly' : 'withText';
  const SIZING_MAP = {
    'withText': {
      'sm': {
        'padding': 'px-1.5 py-0.5',
        'icon': 'w-3 h-3',
        'text': 'text-sm'
      },
      'md': {
        'padding': 'px-3 py-1',
        'icon': 'w-5 h-5',
        'text': 'text-md'
      },
      'lg': {
        'padding': 'px-3 py-1',
        'icon': 'w-6 h-6',
        'text': 'text-lg'
      },
    },
    'iconOnly': {
      'sm': {
        'padding': 'px-1.5 py-1.5',
        'icon': 'w-3 h-3',
        'text': 'text-sm'
      },
      'md': {
        'padding': 'px-1.5 py-1.5',
        'icon': 'w-5 h-5',
        'text': 'text-md'
      },
      'lg': {
        'padding': 'px-1.5 py-1.5',
        'icon': 'w-6 h-6',
        'text': 'text-lg'
      },
    }
  };
  const sizing = SIZING_MAP[buttonType][size];
</script>

<button on:click class="inline-flex justify-center flex-row items-center gap-1 {sizing.padding} border text-gray-700 border-gray-400 border-dashed rounded-full hover:text-orange-700 hover:border-orange-700 {sizing.text}">
  {#if $$slots.extra}
    <slot name="extra"/>
  {:else if extra}
    <span class="{sizing.text} text-gray-300">{extra}</span>
  {/if}
  {#if $$slots.main}
    <slot name="main"/>
  {:else if text}
    <span>{text}</span>
  {/if}
  {#if $$slots.icon}
    <div class="{sizing.icon}">
      <slot name='icon'/>
    </div>
  {/if}
</button>

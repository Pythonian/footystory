(function($){
	$('.like-btn').on( 'mouseenter', unlike );
	$('.like-btn').on( 'mouseleave', like );

	function unlike() {
		var $this = $(this);

		$this.removeClass('primary');
		$this.addClass('tertiary');
		$this.text('Unlike');
	}

	function like() {
		var $this = $(this);

		$this.removeClass('tertiary');
		$this.addClass('primary');
		$this.text('Liked');
	}
})(jQuery);